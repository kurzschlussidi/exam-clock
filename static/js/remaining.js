remainingTime(appConfig.end_time, appConfig.show_remaining, appConfig.show_confetti);

function remainingTime(end_time_str, show_remaining, show_confetti)
{
    end_times = end_time_str.split(':')
    var end_time = new Date();
    var live_time = new Date();
    end_time.setHours(end_times[0]);
    end_time.setMinutes(end_times[1]);
    end_time.setSeconds(end_times[2]);
    end_time.setMilliseconds(0);
    time_diff = (end_time - live_time) / 1000;
    if (show_remaining == 'y') {
        if (Math.floor(time_diff)>=120) { // A lot of time left
            time_diff = Math.floor(time_diff/60)
            document.getElementById("time_remaining").innerHTML=time_diff + ' Minuten';
//        } else if (Math.floor(time_diff) == 1) { // between 1 and 2 minutes left
//            time_diff = Math.floor(time_diff)
//            document.getElementById("time_remaining").innerHTML=time_diff + ' Minute';
        } else if (time_diff > 0){ //under two minutes left
            time_diff = Math.floor(time_diff);
            console.log(time_diff);
            document.getElementById("time_remaining").innerHTML=time_diff + ' Sekunden';
        } else { //time is over
            document.getElementById("time_remaining").innerHTML='Prüfung Vorbei';
            if (show_confetti == 'y') {
                confetti();
            }
            setTimeout(function() {
                window.location.replace(appConfig.redirect_url);
            }, 5000); // Wait 5 seconds before redirecting
        }
    } else {
        if (time_diff < 0) {
            window.location.replace(appConfig.redirect_url);
        }
    }
    t=setTimeout(function(){remainingTime(appConfig.end_time, appConfig.show_remaining)},100);
}

function confetti() {
    var end = Date.now() + (4 * 1000); // Run confetti for 4 seconds
    var colors = ['#bb0000', '#ffffff'];

    (function frame() {
        confetti({
            particleCount: 2,
            angle: 60,
            spread: 55,
            origin: { x: 0 },
            colors: colors
        });
        confetti({
            particleCount: 2,
            angle: 120,
            spread: 55,
            origin: { x: 1 },
            colors: colors
        });

        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    })();
}
