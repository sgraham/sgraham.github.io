---
layout: post
---

So, I watched a few of Rich&#8217;s videos on <a
href="http://clojure.org/">Clojure</a> a couple months back, but I finally got
an afternoon to spend trying it out.

I skimmed through <a href="http://rubyquiz.com">Ruby Quiz</a> to find an
interesting but simple problem, and I decide to write a <a
href="http://www.rubyquiz.com/quiz5.html">Sokoban</a> clone.

My initial thought was to do it as a gui app, but I haven&#8217;t written any
Java code since JDK 1.0-alpha in late 1995, and honestly, I didn&#8217;t
really feel like putting effort into learning the Java GUI API only to end up
with a bizarrely emulated, slightly broken GUI.

So, I grabbed <a
href="http://github.com/weavejester/compojure/tree/master">Compojure</a> off
of git, and made the UI a hack webapp. (Yes, it&#8217;s bizarrely emulated and
slightly broken still, but at least it was easy to write).

First, have a look at the result: <a
href="http://h4ck3r.net:8000/">Clojban!</a>

If you care, the (probably horrible and un-idiomatic) code follows.

{% highlight clojure %}
(ns clojban
  (:use (compojure html
                   http
                   file-utils)
        (clojure.contrib str-utils
                         seq-utils)
        (clojure set))
  (:import (java.util.regex Pattern)))

(defstruct pos :x :y)
(defstruct level
           :player ; pos
           :boxes  ; set-of-pos
           :goals  ; set-of-pos
           :walls  ; set-of-pos
           )

(defn explode
  "return a pos/type seq for each char in the line"
  [y line]
  (map (fn [x y type] (vector (struct pos x y) type))
       (iterate inc 0) (repeat y) line))

(defn line-explode
  "call explode on each line with the appropriate y"
  [lines]
  (let [linesplit (. Pattern compile "\n" (. Pattern MULTILINE))] ; must be a better way?
    (reduce into
            (map explode
                 (iterate inc 0)
                 (. linesplit split lines)))))

(defn filter-level
  "extracts a set of the pos's that match types"
  [expl-level type1 type2 &amp; type3]
  (set (map first
            (filter (fn [item]
                      (or (= (second item) type1)
                          (= (second item) type2)
                          (= (second item) type3)))
                    expl-level))))

(defn load-levels
  "load and return seq of level's"
  [filename]
  (let [contents (slurp filename)
        levelsplit (. Pattern compile "^$\n" (. Pattern MULTILINE)) ; each level separated by blank line
        levels (seq (. levelsplit split contents))]

    (map (fn [levelstr]
           (let [expl-level (line-explode levelstr)]
             (struct-map level
                         :player (first (filter-level expl-level \@ \+))
                         :boxes (filter-level expl-level \o \*)
                         :goals (filter-level expl-level \. \* \+)
                         :walls (filter-level expl-level \# \#))))
         levels)))

(def Levels (load-levels "sokoban_levels.txt"))
(def LvlWidth 19)
(def LvlHeight 16)
(def PlayerRenderOpen "♦")
(def PlayerRenderGoal "♦")
(def BoxRenderOpen "▨")
(def BoxRenderGoal "▨")
(def WallRender "█")
(def GoalRender "░")

(defn level-index [x y] (+ (* y LvlWidth) x))



(defn render-level-layer
  "my, what an insane level representation i have here"
  [target items if-empty if-full]
  (loop [target target
         remain (seq items)]
    (if remain
      (let [x (:x (first remain))
            y (:y (first remain))
            i (level-index x y)
            at (target i)]
        (recur (assoc target i (if (= at \space) if-empty if-full))
               (rest remain)))
      target)))

(defn render-level
  [lvl]
  (let [finallevel (reduce (fn [lvl data] (render-level-layer lvl (nth data 0) (nth data 1) (nth data 2))) ; todo how to splat `data'
                           (vec (replicate (* LvlWidth LvlHeight) \space))
                           `((~(:walls lvl) ~WallRender ~WallRender)
                             (~(:goals lvl) ~GoalRender ~GoalRender)
                             (~(:boxes lvl) ~BoxRenderOpen ~BoxRenderGoal)
                             (~(set (list (:player lvl))) ~PlayerRenderOpen ~PlayerRenderGoal)))]
    (dotimes y LvlHeight
      (print "")
      (dotimes x LvlWidth
        (print "")
        (print (finallevel (level-index x y)))
        (print ""))
      (print ""))))

(def AsciiToDx {72 -1,
                76  1,
                75  0,
                74  0})
(def AsciiToDy {72  0,
                74  1,
                75  -1,
                76  0})

(defn do-player-move
  "handle player movement, input is int ascii code for HJKL."
  [level input]
  (let [dx (get AsciiToDx input)
        dy (get AsciiToDy input)
        curpos (:player level)
        candidatepos (struct pos (+ (:x curpos) dx) (+ (:y curpos) dy))
        pastcandidatepos (struct pos (+ (:x curpos) dx dx) (+ (:y curpos) dy dy))
        walls (:walls level)
        boxes (:boxes level)]
    (if (walls candidatepos)
      level
      (if (boxes candidatepos)
        (if (or (walls pastcandidatepos) (boxes pastcandidatepos))
          level
          (assoc
            (assoc level :boxes (conj (disj boxes candidatepos) pastcandidatepos)) ; move box
            :player candidatepos)) ; and player
        (assoc level :player candidatepos))))) ; only player

(def JSCode "
function postwith (p) {
  var myForm = document.createElement('form');
  myForm.method='post';
  myForm.action='/';
  for (var k in p) {
    var myInput = document.createElement('input');
    myInput.setAttribute('name', k);
    myInput.setAttribute('value', p[k]);
    myForm.appendChild(myInput);
  }
  document.body.appendChild(myForm) ;
  myForm.submit() ;
  document.body.removeChild(myForm) ;
}

function handlekey(e) {
  if (!e) var e = window.event
  if (e.keyCode) code = e.keyCode;
  else if (e.which) code = e.which;
  if (code == 37) code = 72;
  if (code == 38) code = 75;
  if (code == 39) code = 76;
  if (code == 40) code = 74;
  if (code == 72 || code == 74 || code == 75 || code == 76 || code == 82 || code == 65 || code == 90) postwith({'code': code});
}
")

(defn restart-level [session]
  (alter session assoc :curlevel (or (session :curlevel) 0))
  (alter session assoc :complete (or (session :complete) (set nil)))
  (alter session assoc :nummoves 0)
  (alter session assoc :level (nth Levels (or (session :curlevel) 0))))

(defn next-level [session]
  (alter session assoc :curlevel (min
                                   (inc (session :curlevel))
                                   (- (count Levels) 1)))
  (restart-level session))

(defn prev-level [session]
  (alter session assoc :curlevel (max (dec (session :curlevel)) 0))
  (restart-level session))

(defservlet clojban-servlet
  (POST "/"
        (dosync
          (let [prevlevel (session :level)
                keycode (. Integer parseInt (params :code))]
            (if (= keycode 82)
              (restart-level session)
              (if (= keycode 65)
                (prev-level session)
                (if (= keycode 90)
                  (next-level session)
                  (let [moveresult (do-player-move prevlevel keycode)]
                    (if (= 0 (count (difference (:boxes moveresult) (:goals moveresult))))
                      (do
                        (alter session assoc :complete (conj (session :complete) (session :curlevel)))
                        (next-level session))
                      (do
                        (alter session assoc :nummoves (inc (session :nummoves)))
                        (alter session assoc :level moveresult)))))))))
        (redirect-to "/"))
  (GET "/"
       (let [levelstate (or (session :level) (dosync (restart-level session) (session :level)))]
         [{"Content-Type" "text/html"}
          (html
            (doctype :xhtml-transitional)
            [:html {:xmlns "http://www.w3.org/1999/xhtml" :lang "en"}
             [:head
              [:title "Clojban!"]
              [:meta {:http-equiv "Content-Type", :content "text/html; charset=utf-8"}]
              [:script {:type "text/javascript"} JSCode]]
             [:body {:onkeydown "handlekey(event);" :style "font-family: arial; font-size: 13px;"}
              [:h1 {:style "font-family: arial;"} "Clojban"]
              [:p "This is a silly <i>Sokoban</i> implemented in " (link-to "http://clojure.org" "Clojure") ". It's hitting the server every time you move (rather than Javascript) so it might not respond too quickly. The unicode box drawing craziness looks OK in FF, and reasonable in IE, but not so hot in Chrome/Webkit. Sorry."]
              [:table {:style "border-style: none; font-size: 36px; font-family: courier; padding: 0px 0px 0px 0px; margin:0px 0px 0px 0px; line-height: 1em;"
                       :border "0"
                       :cellpadding "0"
                       :cellspacing "0"}
               (with-out-str (render-level levelstate))]
              [:p "Use arrow keys or hjkl to move all the boxes into the goals. Press r to restart level, or a/z to give up and skip through levels."]
              [:p "Level: " (session :curlevel)]
              [:p "Moves: " (session :nummoves)]
              [:p "Completed: " (str-join " " (map (fn [i]
                                                     (let [complete (session :complete)]
                                                       (format "%d"
                                                               (if (complete i) "green" "#ccc")
                                                               i)))
                                                   (range (count Levels))))]
              ]])]))
  (ANY "*"
       (page-not-found)))
{% endhighlight %}

