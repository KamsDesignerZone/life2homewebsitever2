async function initialise_ui() {

}

async function submit() {
    let form = document.querySelector('#contact_form');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    let appointmentData = get_form_data();
    let appointment =  frappe.call({
        method: 'life2homewebsitever2.www.quotes.life2home_get_quotes.get_quotes',
        args: {
            'contact': appointmentData,
        },
        callback: (response)=>{
            console.log(response);
            setTimeout(()=>{
                let redirect_url = "/quotes/life2home_get_quotes_confirmation?doc_name="+response.message.name;
                window.location.href = redirect_url;},
                3
                )
            },
        error: (err)=>{
            frappe.show_alert("Something went wrong please try again");
            button.disabled = false;
        }
    });
}

function get_form_data() {
    contact = {};
    let inputs = ['name', 'customer_phone_number', 'email', 'site_type', 'site_configuration'];
    inputs.forEach((id) => console.log(document.getElementById(`${id}`).value))
    inputs.forEach((id) => contact[id] = document.getElementById(`${id}`).value)
    return contact
}
