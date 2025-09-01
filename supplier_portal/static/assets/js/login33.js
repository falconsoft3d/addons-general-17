 $(document).ready(function() {
    loadSettings();
});

function loadSettings() {
    var portal_login = localStorage.portal_login;
    var id = localStorage.id;

    if (portal_login && portal_pass && id) {
        window.location.href = "/portal/attendance/" + id;
    }
}

function saveSettings() {
    // prevent default action
    event.preventDefault();
    jQuery('#error').remove();

    var email = $("#portal_login").val();
    var password = $("#portal_pass").val();
    var csrf_token = $('#csrf_token').val();
    console.log("csrf_token", csrf_token)
    console.log("loginUser")
    console.log(email, password)

    // Check if user and password are correct
    // Uncaught TypeError: 'stepUp' called on an object that does not implement interface HTMLInputElement.

    var data = {
        "email": email,
        "password": password,
        "csrf_token": csrf_token
    };

    $.ajax({
        url: '/portal/login/check',
        method: 'post',
        timeout: 0,
        headers: {
            'Content-Type': 'application/json'
        },
        data: `{
                        "params": {
                            "csrt_token": "${csrf_token}",
                            "email": "${email}",
                            "password": "${password}"
                        }
                    }`,
        success: function(response) {
            console.log(response.result.status)
            if (response.result.status == "ok") {
                // Save user and password in local storage encrypted
                localStorage.portal_login = encrypt_data(email);
                localStorage.id = response.result.user;

                // Redirect to attendance page
                window.location.href = "/portal/home/" + response.result.user;
            } else {
                // Insert div with error message
                $('#loginForm').append('<div class="alert alert-danger" role="alert" id="error">Error en credenciales</div>');
            }

        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error");
        }
    });



    console.log("End loginUser")
}

function logout() {
    localStorage.removeItem("portal_login");
    localStorage.removeItem("id");
}