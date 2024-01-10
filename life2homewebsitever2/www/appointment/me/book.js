async function initialise_ui() {
    window.selected_date = undefined;
    window.selected_time = undefined;
    await get_global_variables();
    setup_date_picker();
}

async function get_global_variables() {
    // Using await through this file instead of then.
    window.appointment_settings = (await frappe.call({
        method: 'erpnext.www.book_appointment.index.get_appointment_settings'
    })).message;
    window.timezones = (await frappe.call({
        method:'erpnext.www.book_appointment.index.get_timezones'
    })).message;
    window.default_timezone ="Asia/Calcutta"
}

function getFormatedDate(date) {
            var selectedDate = new Date(date);
            var d = selectedDate.getDate();
            var m =  selectedDate.getMonth();
            m += 1;  // JavaScript months are 0-11
            var y = selectedDate.getFullYear();
            var formattedDate = y + "-" + m + "-" + d
    return formattedDate;
}

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}
  
function setup_date_picker() {
    $('#appointment_date').datepicker({
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        dateFormat: 'dd MM yy',
        minDate: new Date(),
        maxDate: "+45d",
        beforeShowDay: function(date) {
            var day = date.getDay();
            return [(day == 3)];
        },
        onClose: async function(dateText, inst) { 
            populatetimeslots (dateText);
        }
    }).focus(function () {
    });
}

async function populatetimeslots(selectedDate) {
    var formattedDate = getFormatedDate(selectedDate)
    let slots = (await frappe.call({
        method: 'erpnext.www.book_appointment.index.get_appointment_slots',
        args: {
            date: formattedDate,
            timezone: `Asia/Calcutta`
        }
    })).message;
    
    $('#appointment_slot').on('change', function() {
        window.selected_date = getFormatedDate(selectedDate);
        window.selected_time = new Date(this.value).getTime();
    });

    $('#appointment_slot').empty();
    if (slots.length >0){
        window.selected_date = undefined;
        window.selected_time = undefined;
        $.each(slots, function(key, value) {
            if (value.availability) {
                $('#appointment_slot').append(`<option value="${value.time}">${formatAMPM(new Date(value.time))}</option>`);
                if (window.selected_date === undefined)
                    window.selected_date = getFormatedDate(new Date(value.time));
                if (window.selected_time === undefined)
                    window.selected_time = new Date(value.time).getTime();
            }
            else 
                $('#appointment_slot').append(`<option value="${value.time}" disabled>${formatAMPM(new Date(value.time))} - Reserved</option>`);
        });
    } else {
        $('#appointment_slot').append(`<option value="-1" disabled selected>No Slots Available For This Date</option>`);                
    }

}
const convertBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);

        fileReader.onload = () => {
            resolve(fileReader.result);
        };

        fileReader.onerror = (error) => {
            reject(error);
        };
    });
};

async function startFileUpload() {
    console.log('Starting File Upload')
    var documentData = new FormData();
    documentData.append('file', $('input#catalogue.findDocumentOnboarding')[0].files[0]);
    console.log(documentData)
    var file = $('input#catalogue.findDocumentOnboarding')[0].files[0];
    const base64FileData = await convertBase64(file);

    var qs = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=', 2);
            if (p.length == 1)
                b[p[0]] = "";
            else
                b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'));

    console.log(qs);
    
    let appointmentfile =  frappe.call({
        type: "POST",
        //method: "life2homewebsitever2.www.appointment.me.book.upload_catalogue",
        args: {
            cmd: 'life2homewebsitever2.www.appointment.me.book.uploadfile',
            doctype : 'Appointment',
            docname : qs["doc_name"],
            filename : file.name,
            is_private: 0,
            filedata: base64FileData,
            folder:`Home/Catalogues`,
            from_form:0
        },
        callback: (response)=>{
            console.log(response);
            setTimeout(()=>{
                let redirect_url = "/appointment/me/book_confirmation?doc_name="+qs["doc_name"];
                window.location.href = redirect_url;},100)
        },
        error: (err)=>{
            frappe.show_alert("Something went wrong please try again");
            button.disabled = false;
        }
    });
}

function setup_search_params() {

    let search_params = new URLSearchParams(window.location.search);
    let customer_name = search_params.get("name")
    let customer_email = search_params.get("email")
    let detail = search_params.get("details")

    if (customer_name) {
        let name_input = document.getElementById("customer_name");
        name_input.value = customer_name;
        name_input.disabled = true;
    }

    if(customer_email) {
        let email_input = document.getElementById("customer_email");
        email_input.value = customer_email;
        email_input.disabled = true;
    }

    if(detail) {
        let detail_input = document.getElementById("customer_notes");
        detail_input.value = detail;
        detail_input.disabled = true;
    }

}

async function submit() {
    let button = document.getElementById('book_appointment');
    button.disabled = true;
    let form = document.querySelector('#contact_form');
    if (!form.checkValidity()) {
        form.reportValidity();
        button.disabled = false;
        return;
    }
    let appointmentData = get_form_data();
    var selected_date = window.selected_date;
    console.log(new Date(window.selected_time))
    var selected_time = new Date(window.selected_time).getHours() + ':' + new Date(window.selected_time).getMinutes() + ':' + new Date(window.selected_time).getSeconds()
    let appointment =  frappe.call({
        method: 'life2homewebsitever2.www.appointment.me.book.create_appointment',
        args: {
            'date': selected_date,
            'time': selected_time,
            'contact': appointmentData,
            'tz': `Asia/Calcutta`
        },
        callback: (response)=>{
            console.log(response);
            if (response.message.status == "Unverified") {
                frappe.show_alert("Please check your email to confirm the appointment")
            } else {
                frappe.show_alert("Appointment Created Successfully");
            }
            setTimeout(()=>{
                let redirect_url = "/appointment/me/book_confirmation?doc_name="+response.message.name;
                window.location.href = redirect_url;},3)
        },
        error: (err)=>{
            frappe.show_alert("Something went wrong please try again");
            button.disabled = false;
        }
    });
}

function get_form_data() {
    contact = {};
    let inputs = ['name', 'customer_phone_number', 'email', 'appointment_date', 'appointment_slot'];
    inputs.forEach((id) => console.log(document.getElementById(`${id}`).value))
    inputs.forEach((id) => contact[id] = document.getElementById(`${id}`).value)
    return contact
}
