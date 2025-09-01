function MenuLogout() {
    localStorage.removeItem("portal_login");
    localStorage.removeItem("id");
    window.location.href = "/portal/";
}


$(document).ready(function() {
    loadSettingsAttendance();
});


function loadSettingsAttendance() {
    var portal_login = localStorage.portal_login;
    var id = localStorage.id;
    var virtual_user_check =  $("#virtual_user_check").val();

    if (portal_login && id && virtual_user_check == id) {
         $("#user_name").text(decrypt_data(portal_login));
    } else {
        MenuLogout();
    }
}