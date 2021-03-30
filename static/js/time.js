startTime(appConfig.show_seconds);
function startTime(show_seconds)
    {
    var today=new Date();
    var h=today.getHours();
    var m=today.getMinutes();
    var s=today.getSeconds();
    // add a zero in front of numbers<10
    h=checkTime(h);
    m=checkTime(m);
    s=checkTime(s);
    if (show_seconds=='y') {
      document.getElementById("live_clock").innerHTML=h+":"+m+":"+s;
    } else {
      document.getElementById("live_clock").innerHTML=h+":"+m;
    }
    t=setTimeout(function(){startTime(show_seconds)},500);
    }
    
    function checkTime(i)
    {
    if (i<10)
      {
      i="0" + i;
      }
    return i;
    }
