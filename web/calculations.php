<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>King of CollegeBball</title>
    <link rel="stylesheet" href="normalize.css">
    <!--copy to /var/www/html before opening in browser-->
    <!--and copy python programs and css-->
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
        /* foreach($result as $rows){
            echo "<h1 style='font-size: 30px;'>".$rows['Team']."</h1>";
            foreach($rows as $column => $value){
                echo "<p>".$column." = ".$value."<br></p>";
            }
        }*/
        echo "Fetch successful<br>";
    } catch(PDOException $e) {
        echo $sql . "<br>" . $e->getMessage();
    }

    exec("python3 exec_practice.py", $output, $status);
    print_r($output[0]);
    //$output[0] is string

    //New process:
    //  1. python program is run to execute todayScores, createSpreads & createTotals
    //  as one function that adds results to a "working" database (cleared after use)
    //  2.addNolan is run based on (1) and formatschedule database and adds results
    //  to finalNumbers db
    //  3. Access and show
    //


    echo "<h1>".$status."</h1>";
    //------------------Calculations---------------------------
    //TODO:
    //  1. Create nolan db
    //  2. Create odds db (no data if no games)
    
    //TODO : dayscores = todaysScores(fCBB_SCH, kpData) in PHP
    //fCBB_SCH can be in schedule mysql table
    //kpData can be in kenpom mysql table
    //takes kenpom data and schedule and makes calculations based on algorithm

    //TODO : withSpreads = createSpread(dayscores)

    //TODO : withTotals = createTotals(withSpreads)

    //TODO : resultsNolan = addNolan(fNolan, withTotals)
    //fNolan can be in nolan mysql table
    //withTotals will be from function above


    //TODO : odds = getVegas()
    //odds will have to be fetched from odds mysql table 


    //------------------Drop database connection-------------------

    //safe exit from db
    $conn = null;
?>


</body>
</html>