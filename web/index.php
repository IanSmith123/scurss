<?php
date_default_timezone_set('Asia/Shanghai');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>scurss</title>
    <link href="assets/css/bootstrap.css" rel="stylesheet">
    <link href="assets/css/docs.css" rel="stylesheet">
    <style type="text/css">
        body {
            padding-top: 60px;
            padding-bottom: 40px;
            position: relative;
        }
        .affix {
            top: 20px;
            z-index: 9999 !important;
        }
    </style>

    <link href="assets/js/google-code-prettify/prettify.css" rel="stylesheet">
    <link href="assets/css/bootstrap-responsive.css" rel="stylesheet">
    <script src="assets/js/jquery.js"></script>
    <script src="assets/js/bootstrap-transition.js"></script>
    <script src="assets/js/bootstrap-alert.js"></script>
    <script src="assets/js/bootstrap-modal.js"></script>
    <script src="assets/js/bootstrap-dropdown.js"></script>
    <script src="assets/js/bootstrap-scrollspy.js"></script>
    <script src="assets/js/bootstrap-tab.js"></script>
    <script src="assets/js/bootstrap-tooltip.js"></script>
    <script src="assets/js/bootstrap-popover.js"></script>
    <script src="assets/js/bootstrap-button.js"></script>
    <script src="assets/js/bootstrap-collapse.js"></script>
    <script src="assets/js/bootstrap-carousel.js"></script>
    <script src="assets/js/bootstrap-typeahead.js"></script>
    <script src="assets/js/bootstrap-affix.js"></script>
</head>
<body data-spy="scroll" data-target=".bs-docs-sidebar">

<div class="navbar navbar-inverse navbar-fixed-top">
    <div class="navbar-inner">
        <div class="container">
            <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="brand" href="#">SCURSS</a>
            <div class="nav-collapse collapse">
                <ul class="nav">
                    <li class="active"><a href="#">Home</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>

                </ul>
                <!--<form class="form-search pull-right">
                    <input type="text" class="input-medium search-query">
                    <button type="submit" class="btn">Search</button>
                </form>-->
                <!--<form class="navbar-form pull-right">
                    <input class="span2" type="text" placeholder="Username">
                    <input class="span2" type="text" placeholder="Email">
                    <button type="submit" class="btn">Submit</button>
                </form>-->
            </div><!--/.nav-collapse -->
        </div>
    </div>
</div>

<header class="jumbotron masthead">
    <div class="container" style=" text-align:center;">
            <h1>Welcome to SCURSS!</h1>
            <p>川大校内资讯整合推送平台</p>
    </div>

        <!--<p><a href="#" class="btn btn-primary btn-large">Learn more &raquo;</a></p>-->
</header>
<!--<div align="center"> <img src="img/a.jpg" ></div>-->
<div class="container">
    <br />
 <div class="row">
     <div class="span3 bs-docs-sidebar">
        <ul class="nav nav-list bs-docs-sidenav" data-spy="affix" data-offset-top="550">
            <li>
                <a href="#jwc">
                    <i class="icon-chevron-right"></i>
                    " 教务处新闻 "
                </a>
            </li>
            <li>
                <a href="#xsc">
                    <i class="icon-chevron-right"></i>
                    " 学工部新闻 "
                </a>
            </li>
            <li>
                <a href="#cs">
                    <i class="icon-chevron-right"></i>
                    " 计算机学院新闻 "
                </a>
            </li>
            <li>
                <a href="#subscribe">
                    <i class="icon-chevron-right"></i>
                    " 订阅 "
                </a>
            </li>
        </ul>
     </div>
    <!--<div class="row-fluid" style="left: auto">-->
        <div class="span9">
            <section id="jwc">
                <div class="page-header">
                    <a href="http://jwc.scu.edu.cn" target="_blank"><h1>教务处</h1></a>
                </div>
            <?php

            //$conn = pg_connect("host=b.17010.tk port=5432 dbname=scurss user=postgres password=ms17010");
            //$conn = pg_connect("host=108ed.les1ie.com port=5432 dbname=scurss user=postgres password=ms17010");
            $conn = pg_connect("host=pgsqldb port=5432 dbname=scurss user=postgres password=ms17010");
            if(!$conn){echo "ERROR.\n";exit;}
            $result = pg_query($conn,"SELECT newstitle, newsurl, publishtime FROM jwcnews ORDER BY lastupdatetime DESC LIMIT 10;");
            if (!$result){echo "ERROR2.\n";exit;}
            echo "<table width='800' border='0' cellpadding='10' cellspacing='10'><tbody>";
            while ($row = pg_fetch_row($result)){
                $pubdate = date("Y-m-d", $row[2]);
                echo "<tr><td width='600' valign='bottom'><a href='$row[1]' target='_blank'> $row[0] </a></td>
                      <td width='200' align='left' height='20' valign='top'><font color='#999999'>$pubdate</font> </td></tr>";
            }
            echo "</tbody></table>"

            ?>
            </section>

            <section id="xsc">
            <div class="page-header">
                <a href="http://xsc.scu.edu.cn" target="_blank"><h1>学工部</h1></a>
            </div>
            <?php

            $conn = pg_connect("host=pgsqldb port=5432 dbname=scurss user=postgres password=ms17010");
            //$conn = pg_connect("host=108ed.les1ie.com port=5432 dbname=scurss user=postgres password=ms17010");
            if(!$conn){echo "ERROR.\n";exit;}
            $result = pg_query($conn,"SELECT newstitle, newsurl, publishtime FROM xscnews ORDER BY lastupdatetime DESC LIMIT 10;");
            if (!$result){echo "ERROR2.\n";exit;}
            echo "<table width='800' border='0' cellpadding='10' cellspacing='10'><tbody>";
            while ($row = pg_fetch_row($result)){
                $pubdate = date("Y-m-d", $row[2]);
                echo "<tr><td width='600' valign='bottom'><a href='$row[1]' target='_blank'> $row[0] </a></td>
                      <td width='200' align='left' height='20' valign='top'><font color='#999999'>$pubdate</font> </td></tr>";
            }
            echo "</tbody></table>"

            ?>
            </section>

            <section id="cs">
                <div class="page-header">
                    <a href="http://cs.scu.edu.cn" target="_blank"><h1>计算机学院</h1></a>
                </div>
            <?php

            //$conn = pg_connect("host=b.17010.tk port=5432 dbname=scurss user=postgres password=ms17010");
            $conn = pg_connect("host=pgsqldb port=5432 dbname=scurss user=postgres password=ms17010");
            if(!$conn){echo "ERROR.\n";exit;}
            $result = pg_query($conn,"SELECT newstitle, newsurl, publishtime FROM csnews ORDER BY lastupdatetime DESC LIMIT 10;");
            if (!$result){echo "ERROR2.\n";exit;}
            echo "<table width='800' border='0' cellpadding='10' cellspacing='10'><tbody>";
            while ($row = pg_fetch_row($result)){
                $pubdate = date("Y-m-d", $row[2]);
                echo "<tr><td width='600' valign='bottom'><a href='$row[1]' target='_blank'> $row[0] </a></td>
                      <td width='200' align='left' height='20' valign='top'><font color='#999999'>$pubdate</font> </td></tr>";
            }
            echo "</tbody></table>"

            ?>
            </section>





            <section id="subscribe">
                    <form action="post.php" method="post">
                        <fieldset>
                            <legend><h1>订阅</h1></legend>
                            <label>输入你的信息</label>
                            <input type="text" name="username" placeholder="Username">
                            <input type="email" name="usermail" placeholder="Email">
                            <label class="checkbox">
                                <input type="checkbox" name="subscribelist[]" value="jwcnews">四川大学教务处
                            </label>
                            <label class="checkbox">
                                <input type="checkbox" name="subscribelist[]" value="xgbnews">四川大学学工部
                            </label>
                            <label class="checkbox">
                                <input type="checkbox" name="subscribelist[]" value="csnews">四川大学计算机学院
                            </label>
                            <br />
                            <label class="checkbox">
                                <input type="checkbox" name="check[]" value="1">想要建议其他网站？
                            </label>
                            <label>
                                你想要SCURSS添加的网址（例如http://pead.scu.edu.cn）
                            </label>
                            <input type="url" name="url" >
                            <br/>
                            <!--<span class="help-block">这里填写帮助信息.</span> <!-- <label class="checkbox"><input type="checkbox" /> 勾选同意</label> -->
                            <button class="btn" type="submit">提交</button>
                        </fieldset>
                    </form>
            </section>
        </div>
 </div>
</div>



 <!--</div>-->

    <footer class="footer">
        <div class="container">
        <p class="pull-right"><a href="#">Back to top</a> </p>
        <p>2017 scurss</p>
        <p><a href="feed.xml"> 订阅RSS？</a><p>
        </div>
    </footer>


</body>
</html>