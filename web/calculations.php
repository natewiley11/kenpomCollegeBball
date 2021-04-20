<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>King of CollegeBball</title>
    <link rel="stylesheet" href="normalize.css">
    <script src="passwords.js"></script>
    <!--copy to /var/www/html before opening in browser-->
</head>
<body>
<h1>Working...</h1>
<?php
    include 'database.php';
    //establish connection to db
    try {
        $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
        echo "Connected to $dbname at $host successfully\n";
    } catch (PDOException $pe) {
        die("Could not connect to the database $dbname :" . $pe->getMessage());
    }

    //access database
    try{
        // set the PDO error mode to exception
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $sql = "SELECT * from kenpom where Team='Gonzaga' or Team='Villanova';";
        $query = $conn->prepare($sql);
        $data = $query->execute();
        $result = $query->fetchAll(PDO::FETCH_ASSOC);
        foreach($result as $rows){
            echo "<h1 style='font-size: 30px;'>".$rows['Team']."</h1>";
            foreach($rows as $column => $value){
                echo "<p>".$column." = ".$value."<br></p>";
            }
        }

        echo "Fetch successful<br>";
    } catch(PDOException $e) {
        echo $sql . "<br>" . $e->getMessage();
    }

    //safe exit
    $conn = null;
?>


</body>
</html>