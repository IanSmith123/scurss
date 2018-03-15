<html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="5;url=index.php">
        <title>post</title>
    </head>

    <body>
    <?php
        //$conn = pg_connect("host=b.17010.tk port=5432 dbname=scurss user=postgres password=ms17010");
        $conn = pg_connect("host=pgsqldb port=5432 dbname=scurss user=postgres password=ms17010");
        if(!$conn){echo "ERROR.\n"; exit;}
        $username = $_POST["username"];
        if (!preg_match("/^[a-zA-Z ]*$/",$username)) {
            $usernameErr = "只允许字母和空格！";
        }
        $assoc_array['username']=$username;
        //$result1 = pg_query($conn, "SELECT username FROM userlist WHERE username="+$username+" ;");
        $email = $_POST["usermail"];
        $assoc_array['usermail']=$email;
        /*if (!preg_match("/([\w\-]+\@[\w\-]+\.[\w\-]+)/",$email)) {
            $emailErr = "无效的 email 格式！";
        }*/
        //$result2 = pg_query($conn, "SELECT usermail FROM userlist WHERE username="+$usermail+" ;");
        //if($result1){echo "Username has been used.\n";exit;}
        //elseif($result2){echo "Email has been used.\n";exit;}
        //else {
            $list = $_POST["subscribelist"];
            $list2 = implode(",",$list);
            //echo $list2;
            $assoc_array['subscribelist']=$list2;
            $time = time();
            //$website = $_POST['website'];
            //echo $website;
            //$assoc_array = $_POST;
            //$result3 = pg_query($conn, "SELECT uuid FROM userlist ORDER BY uuid DESC LIMIT 1;");
            /*if(!$result3){
                $assoc_array['uuid']="1";
            }
            else{
                $row = pg_fetch_row($result3);
                $row[0]++;
                $assoc_array['uuid']=$row[0];
            }*/
            $uuid = uniqid();
            $assoc_array['uuid']= $uuid;

            //$assoc_array['username']=$username;
            $assoc_array['regtime']=$time;
            //$assoc_array['usermail']=$email;
            //$assoc_array['subscribelist']=$website;
            /*function db_build_insert($table,$array)
            {

                $str = "insert into $table ";
                $strn = "(";
                $strv = " VALUES (";
                while(list($name,$value) = each($array)) {

                    if(is_bool($value)) {
                       $strn .= "$name,";
                       $strv .= ($value ? "true":"false") . ",";
                       continue;
                     }

                   if(is_string($value)) {
                        $strn .= "$name,";
                        $strv .= "'$value',";
                        continue;
                    }
                    if (!is_null($value) and ($value != "")) {
                        $strn .= "$name,";
                        $strv .= "$value,";
                        continue;
                    }
                }
                $strn[strlen($strn)-1] = ')';
                $strv[strlen($strv)-1] = ')';
                $str .= $strn . $strv;
                return $str;

            }*/
            //$table = ''
            //$insertsql = db_build_insert()
            $res = pg_insert($conn, 'userlist', $assoc_array );
            $check = $_POST['check'];
            if($check[0]){
                $assoc_array2['commiturl'] = $_POST['url'];
                $assoc_array2['uuid'] = $uuid;
                $assoc_array2['username'] = $assoc_array['username'];
                $res2 = pg_insert($conn, 'tocrawl', $assoc_array2);
            }

            if(!$check[0] && $res || $res && $res2){
                //$url = 'http://108ed.les1ie.com:5431/reg';
                $url = 'http://init_mail_server/reg';
                $html = file_get_contents($url);
                echo $html;
                echo "注册成功！\n返回中 \n";
            }
            else{echo "注册失败！\n返回中 \n";}
        //}
    ?>

    </body>
</html>

