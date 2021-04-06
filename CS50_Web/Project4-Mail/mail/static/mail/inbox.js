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
  clear_page("New Email", '#compose-view')

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function sent_email(event) {
    // Get user input
    recipients = document.querySelector('#compose-recipients').value
    subject = document.querySelector('#compose-subject').value
    body = document.querySelector('#compose-body').value

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
        // If error happens
        if (result.error) {
            // Display error message
            alertMessage = document.querySelector('#message')
            alertMessage.classList.add('alert-danger')
            alertMessage.innerHTML = result.error
            alertMessage.style.display = 'block'
        } else {
            // Email been sent successfully, redirect to sent page
            load_mailbox('sent', message=result.message)
        }
        // Print result
        // console.log(result);
      });

    // Prevent default submit behaviour
    event.preventDefault()
}

toggle_archive = function(id, event) {
    console.log(`id is ${id}`);

    // Get current status of the email
    fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {
            console.log(email)
            // 1. Change the archive status based on the current status
            fetch(`/emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: !email.archived
                })
              })
            // 2. Load the inbox page
            load_mailbox('inbox')
        })
}

// toggle_reply = function(event, )

email_detail = function(email) {
    return function curried_func(e) {
        console.log('This element has been clicked!')
        
        // 1. Create a email detail element
        let email_element = document.createElement('div');
        // 2. Change the content of the email-container to the email just created
        const {sender, recipients, subject, timestamp, body} = email

        // Show the email-container, unshow the mail box views
        clear_page(subject, '#email-container');

        document.querySelector('#from_value').innerHTML = sender
        document.querySelector('#to_value').innerHTML = recipients
        document.querySelector('#subject_value').innerHTML = subject
        document.querySelector('#timestamp_value').innerHTML = timestamp
        document.querySelector('#email-content').innerHTML = body
    
        // 3. Change the button to archive/unarchive
        archive_button = document.querySelector('#archive')
        console.log(email.id);
        archive_button.addEventListener('click', toggle_archive.bind(event, email.id), false)
        if (email.archived) {
            archive_button.innerHTML = "Unarchive"
        } else {
            archive_button.innerHTML = "Archive"
        }
    
        // 5. Mark the email as read in the database
        fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
    }
}

function load_mailbox(mailbox, message=null) {
    
  // 1. Show the mailbox and hide other views
  clear_page(mailbox, '#emails-view', message);

  // 2. Show records of emails
  // 3.1 Make API calls (Fetch all emails from the given mail box)
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Print emails
        console.log(emails);

        // When no emails exist
        emails_element = document.querySelector('#emails')
        if (emails.length == 0) {
            emails_element.style.display = 'none'
        } else {
            emails_element.style.display = 'block'
            // Email records found
            for (email of emails) {
    
                // Record row (to be added in record table)
                let record_row = document.createElement("li")
                // Single record div (contains three text node of information)
                let record = document.createElement('div')
    
                let sender = document.createElement('div')
                sender.classList.add('title')
                sender.appendChild(document.createTextNode(email.sender))
                let subject = document.createElement('div')
                subject.classList.add('subject')
                subject.appendChild(document.createTextNode(email.subject))
                let timestamp = document.createElement('div')
                timestamp.classList.add('timestamp')
                timestamp.appendChild(document.createTextNode(email.timestamp))

                // Differenciate read/unread emails
                if (email.read) {
                    record.classList.add('read')
                } else {
                    record.classList.add('unread')
                }
    
                // Make up single record
                record.appendChild(sender)
                record.appendChild(subject)
                record.appendChild(timestamp)
                record.classList.add('email-record')
                // When a email record is been clicked
                record.addEventListener('click', email_detail(email));
                // Make up the record row
                record_row.appendChild(record)
                // Add the record into the email table
                emails_element.appendChild(record_row)
            }
        }

    });

}

// #emails-views, #emails, #compose-view, #message, #email-container
function clear_page(title, block_remains, message=null) {
    all_blocks = ['#email-container', '#compose-view', '#emails']

    // 1. wipe all emails and remove event listeners
    let emails = document.querySelector('#emails')
    // Remove event listeners
    for (let child of emails.children) {
        child.children[0].removeEventListener('click', email_detail);
    }
    // Wide out everything
    emails.innerHTML = '';

    // @TO-DO: removeEventLisenter for archive and reply (function been bind to eventlisenters)
    // 2. Remove eventlisteners
    document.querySelector('#archive').removeEventListener('click', toggle_archive, false)
    // document.querySelector('#reply').removeEventListener('click', toggle_archive_handler, false)
    console.log("Clearing page: removing toggle_archive eventListener...");

    // 3. Show the page title
    document.querySelector('#emails-view').innerHTML = `<h3>${title.charAt(0).toUpperCase() + title.slice(1)}</h3>`;

    // 4. Check if alert message needs to be displayed
      // Show/Not show alert message (when redirecting from other 'pages')
    alertMessage = document.querySelector('#message');
    if (message) {
        // Display success message
        alertMessage.classList.add('alert-success')
        alertMessage.innerHTML = result.message
        alertMessage.style.display = 'block'
    } else {
        alertMessage.style.display = 'none';
    }

    // 5. Change the view display status
    for (let block of all_blocks) {
        if (block == block_remains) {
            document.querySelector(block_remains).style.display = 'block'
        } else {
            document.querySelector(block).style.display = 'none'
        }
    }


}