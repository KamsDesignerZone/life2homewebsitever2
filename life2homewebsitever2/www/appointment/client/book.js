async function initialise_ui() {
    await get_global_variables();
    setup_date_picker();
}

async function get_site_type() {
    // Using await through this file instead of then.
    window.appointment_settings = (await frappe.call({
        method: 'erpnext.www.book_appointment.index.get_appointment_settings'
    })).message;
    window.timezones = (await frappe.call({
        method:'erpnext.www.book_appointment.index.get_timezones'
    })).message;
    window.default_timezone ="Asia/Calcutta"
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
            return [(day != 3)];
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
    $('#appointment_slot').empty();
    if (slots.length >0){
        $.each(slots, function(key, value) {
            if (value.availability)
                $('#appointment_slot').append(`<option value="${formatAMPM(new Date(value.time))}">${formatAMPM(new Date(value.time))}</option>`);
            else 
                $('#appointment_slot').append(`<option value="${formatAMPM(new Date(value.time))}" disabled>${formatAMPM(new Date(value.time))} - Reserved</option>`);
        });
    } else {
        $('#appointment_slot').append(`<option value="-1" disabled selected>No Slots Available For This Date</option>`);                
    }

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
    //button.disabled = true;
    let form = document.querySelector('#contact_form');
    if (!form.checkValidity()) {
        form.reportValidity();
        button.disabled = false;
        return;
    }
    let appointmentData = get_form_data();
    // let appointment =  frappe.call({
    //     method: 'erpnext.www.book_appointment.index.create_appointment',
    //     args: {
    //         'date': window.selected_date,
    //         'time': window.selected_time,
    //         'contact': appointmentData,
    //         'tz':window.selected_timezone
    //     },
    //     callback: (response)=>{
    //         if (response.message.status == "Unverified") {
    //             frappe.show_alert("Please check your email to confirm the appointment")
    //         } else {
    //             frappe.show_alert("Appointment Created Successfully");
    //         }
    //         setTimeout(()=>{
    //             let redirect_url = "/";
    //             if (window.appointment_settings.success_redirect_url){
    //                 redirect_url += window.appointment_settings.success_redirect_url;
    //             }
    //             window.location.href = redirect_url;},5000)
    //     },
    //     error: (err)=>{
    //         frappe.show_alert("Something went wrong please try again");
    //         button.disabled = false;
    //     }
    // });
}

function get_form_data() {
    contact = {};
    let inputs = ['client_name', 'phone', 'email', 'appointment_date', 'appointment_slot', 'site_type', 'site_configuration', 'site_locality', 'site_fulladdress', 'project_completion_priority'];
    inputs.forEach((id) => console.log(document.getElementById(`${id}`).value))
    inputs.forEach((id) => contact[id] = document.getElementById(`${id}`).value)
    return contact
}
