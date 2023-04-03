<?php
    session_start();
    $errors = array();
    $errors[0] = "";
    if (isset($_POST["login"])){
        // retrieve data from the form
        $user = $_POST["user"];
        $password = $_POST["password"];

        // validate the data
        if (trim($_POST["user"]) == "")
            $errors[0] = "Please enter the user name";
        elseif (trim($_POST["password"]) == "")
            $errors[0] = "Please enter the password";

        if ($errors[0] == ""){
            $con = mysqli_connect("localhost", "root", "", "hospital_database");
            $query = mysqli_query($con, "select * from users where user_name = '$user' and password = '$password'");
            $rec = mysqli_fetch_array($query);
    
            if ($rec['user_name'] == $user && $rec['password'] == $password){
                $_SESSION['user_id'] = $user;
                header('Location: dashboard.php');
                exit();
            }else{
                $errors[0] = "Invalid user name and/or password";
            }
        }
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link rel="stylesheet" type="text/css" href="css/login.css">
</head>
<body>
    <div class="bg-image">
        <div class="bg-image-layer"></div>
    </div>
    
    <div>
        <div class="content">
            <h1>Hospital++</h1>
            <form method="POST" action="<?php print ($_SERVER['PHP_SELF']); ?>">
                <input type="text" placeholder="Username" name="user" value="<?php
                    if (isset($_POST['login'])){
                        print $_POST['user'];
                    }
                ?>"><br>
                <input type="password" placeholder="Password" name="password"><br>
                <span class="error-span"><?php print($errors[0]) ?></span><br>
                <input type="submit" value="LOGIN" name="login">
            </form>
        </div>
    </div>
</body>
</html>