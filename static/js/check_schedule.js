let doctorID;
let dateSelect = document.getElementById('dateSelect');
let timeSelect = document.getElementById('timeSelect');
dateSelect.disabled = true;
timeSelect.disabled = true;

let usedDateTime = JSON.parse(JSON.parse(document.getElementById('usedDateTime').textContent));

function send_request(url) {
    return fetch(url,
        {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        })
        .then((response) => {
            return response.json()
        })
        .catch(error => console.warn(error));
      }

document.getElementById('doctorSelect').addEventListener('change', function() {
    doctorID = this.value;
    document.getElementById('dateSelect').disabled = false;
    if ($('#datepicker').datepicker('getDate') != null) {
      $('#datepicker').datepicker('setDate', null);
    }
});

$(function() {
    $('#datepicker').datepicker({
        startDate: new Date(),
        daysOfWeekDisabled: [0,6],
        weekStart: 1,
        format: 'dd/mm/yyyy',
        autoclose: true,
    });

    $('#datepicker').on('changeDate', function(){
        let dateTime = new Date($('#datepicker').datepicker('getDate'));
        let strDateTime = dateTime.getDate() + '/' + (dateTime.getMonth() + 1) + '/' + dateTime.getFullYear();
        let timeNow = new Date(Date.now());
        let hours = timeNow.getHours();
        if (hours<10) hours = "0" + hours;
        let strTimeNow = hours + ':' + timeNow.getMinutes() + ':' + timeNow.getSeconds();
        let idx = timeSelect.selectedIndex

        timeSelect.disabled = false;
        timeSelect.options[idx].innerText = 'Choose time';

        if (strTimeNow > '17:00:00' && dateTime.getDate() === timeNow.getDate()) {
            timeSelect.options[idx].innerText = 'No available time today';
            timeSelect.disabled = true;
        }
        for (let i = 1; i < 10; i++) {
            let unavailableTime = timeSelect.options[i];
            unavailableTime.removeAttribute('disabled');
            if (unavailableTime.value < strTimeNow && dateTime.getDate() === timeNow.getDate()) {
                unavailableTime.setAttribute('disabled', 'disabled');
            };
        }

        if (usedDateTime['result']) {
            for (let i = 0; i < usedDateTime['result'].length; i++) {
                if (usedDateTime['result'][i]['date'] === strDateTime) {
                    for (let j = 0; j < timeSelect.length; j++) {
                        if (timeSelect.options[j].value === usedDateTime['result'][i]['time']) {
                            let unavailableTime = timeSelect.options[j];
                            unavailableTime.setAttribute('disabled', 'disabled');
                        }
                    }
                }
            }
        }

        async function activate() {
            let schedule = await send_request(`/schedule/${doctorID}`);
            if (schedule['result']) {
                for (let i = 0; i < schedule['result'].length; i++) {
                    if (schedule['result'][i]['date'] === strDateTime) {
                        for (let j = 0; j < timeSelect.length; j++) {
                            if (timeSelect.options[j].value === schedule['result'][i]['time']) {
                                let unavailableTime = timeSelect.options[j];
                                unavailableTime.setAttribute('disabled', 'disabled');
                            }
                        }
                    }
                }
            }
        }
        activate();
    });
});