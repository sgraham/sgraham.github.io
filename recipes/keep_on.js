(function(){
var fullScreenButton = document.createElement("button");
fullScreenButton.innerText = 'Enter Full Screen';
document.body.insertBefore(fullScreenButton, document.body.childNodes[0]);

fullScreenButton.addEventListener('click', () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
    fullScreenButton.textContent = 'Leave Full Screen';
  } else {
    document.exitFullscreen();
    fullScreenButton.textContent = 'Enter Full Screen';
  }  
});

if ('wakeLock' in navigator && 'request' in navigator.wakeLock) {  
  let wakeLock = null;
  
  const requestWakeLock = async () => {
    try {
      wakeLock = await navigator.wakeLock.request('screen');
      wakeLock.addEventListener('release', (e) => {
        console.log(e);
        console.log('Wake Lock was released');                    
      });
      console.log('Wake Lock is active');      
    } catch (e) {      
      console.error(`${e.name}, ${e.message}`);
    } 
  };
  
  requestWakeLock();
  
  const handleVisibilityChange = () => {    
    if (wakeLock !== null && document.visibilityState === 'visible') {
      requestWakeLock();
    }
  };    
  
  document.addEventListener('visibilitychange', handleVisibilityChange);
  document.addEventListener('fullscreenchange', handleVisibilityChange);
} else {  
  console.error('Wake Lock API not supported.');
}
})();
