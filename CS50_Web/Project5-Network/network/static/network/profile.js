document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to follow/unfollow certain user
    document.querySelector('#follow').addEventListener('click', follow);
    document.querySelector('#unfollow').addEventListener("submit", unfollow);

  });

function follow(event) {
    username = document.querySelector('#username')
    fetch(`/follow/${username}`, {
        method: 'PUT',
      })
}

function unfollow(event) {
    username = document.querySelector('#username')
    fetch(`/unfollow/${username}`, {
        method: 'PUT',
      })
}