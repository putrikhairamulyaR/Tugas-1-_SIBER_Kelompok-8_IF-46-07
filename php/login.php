//untuk meletakkan logika login dan autentikasi
<?php
    //untuk logika login dan autentikasi
    include 'app.php';
    //untuk mulai sesi agar penggguna bisa akses
    session_start();
    
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        //mengambil data username dan password dari form
        $username = $_POST['username'];
        $password = $_POST['password'];
        //cek apakah username dan password tersebut sama dengan yang ada di hard codenya
        $is_logged_in = login($username, $password); 
        
        if ($is_logged_in) {
            //ketika username dan password sama, nilai login true untuk 
            //memberikan tanda bahwa pengguna sudah login dan diarahkan masuk ke halaman index
            $_SESSION['user_logged_in'] = true; 
            header('Location: index.php'); 
            exit(); 
        } else {
            // jika belum login diarahkan kembali ke halaman login untuk melakukan login terlebih dahulu.
            header('Location: login.php'); 
            exit();
        }
    }
    
?>

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Selamat datang, silahkan login terlebih dahulu!</h1>
    <!-- Form Luntuk melakukan login, untuk memasukkan username dan password -->
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" name="username" required><br>

        <label for="password">Password:</label>
        <input type="password" name="password" required><br>

        <button type="submit">Login</button>
    </form>
</body>
</html>
