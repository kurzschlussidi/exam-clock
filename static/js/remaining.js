remainingTime(appConfig.end_time);

function remainingTime(end_time_str)
{
    end_times = end_time_str.split(':')
    var end_time = new Date();
    var live_time = new Date();
    end_time.setHours(end_times[0]);
    end_time.setMinutes(end_times[1]);
    time_diff = Math.round((end_time - live_time) / 60000);
    if (time_diff > 1) {
        document.getElementById("time_remaining").innerHTML=time_diff + ' Minuten';
    } else if (time_diff == 1){
        document.getElementById("time_remaining").innerHTML=time_diff + ' Minute';
    } else {
        document.getElementById("time_remaining").innerHTML='Prüfung Vorbei';
        // Simulate an HTTP redirect:
        window.location.replace(appConfig.redirect_url);
    }
    t=setTimeout(function(){remainingTime(end_time_str)},500);
}