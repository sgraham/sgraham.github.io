(function(){
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
