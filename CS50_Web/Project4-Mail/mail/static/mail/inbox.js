document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // Compose email sent
  document.querySelector('#compose-form').addEventListener("submit", sent_email);
  // By default, load the inbox
  load_mailbox('inbox');
  

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function sent_email(event) {
    console.log(event)
    // Get user input
    recipients = document.querySelector('#compose-recipients').value
    subject = document.querySelector('#compose-subject').value
    body = document.querySelector('#compose-body').value

    console.log(recipients);
    console.log(subject);
    console.log(body);

    // Make API calls, sending emails through the back end
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            "recipients": recipients,
            "subject": subject,
            "body": body
        })
      })
      .then(response => response.json() )
      .then(result => {
        console.log(result.status);
        // If error happens
        if (result.error) {
            // Display error message
            alertMessage = document.querySelector('#message')
            alertMessage.classList.add('alert-danger')
            alertMessage.innerHTML += result.error
            alertMessage.style.display = 'block'
        } else {
            // Email been sent successfully, redirect to sent page
            load_mailbox('sent', message=result.message)
        }
        // Print result
        console.log(result);
      });

    // Prevent default submit behaviour
    event.preventDefault()
}

function load_mailbox(mailbox, message=null) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show/Not show alert message (when redirecting from other 'pages')
  alertMessage = document.querySelector('#message');
  if (message) {
      // Display success message
    alertMessage.classList.add('alert-success')
    alertMessage.innerHTML += result.message
    alertMessage.style.display = 'block'
  } else {
    alertMessage.style.display = 'none';
  }


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}