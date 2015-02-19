<!--
<table>
<tr>
    <th>Item</th>
    <th>Quantity</th>
</tr>
%for row in rows:
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    </tr>
%end
</table>

-->
<!DOCTYPE HTML>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Customer Detail</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
  
  <!---Header-->
  <nav class="navbar navbar-inverse" role="navigation">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">Brand</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">Seller Detail<span class="sr-only">(current)</span></a></li>
        <li><a href="#">Customer Detail</a></li>
        <li><a href="#">Products Detail</a></li>
      
       </ul>
      <form class="navbar-form navbar-left" role="search">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Search">
        </div>
        <button type="submit" class="btn btn-default">Find</button>
      </form>
      <ul class="nav navbar-nav navbar-right">
        
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Login<span class="caret"></span></a>
          <ul class="dropdown-menu" role="menu">
            <li><a href="#">Seller Login</a></li>
            <li><a href="#">Customer Login</a></li>
            <li class="divider"></li>
            <li><a href="#">Admin Pannel</a></li>
          </ul>
        </li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Registration<span class="caret"></span></a>
          <ul class="dropdown-menu" role="menu">
            <li><a href="#">Seller Registration</a></li>
            <li><a href="#">Product Registration</a></li>
            <li class="divider"></li>
            <li><a href="#">Customer Registration</a></li>
          </ul>
        </li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>

<!-- Pagination-->

    <nav>
      <ul class="pagination">
        <li class="disabled"><a href="#"><span aria-hidden="true">«</span><span class="sr-only">Previous</span></a></li>
        <li class="active"><a href="#">1 <span class="sr-only">(current)</span></a></li>
        <li><a href="#">2</a></li>
        <li><a href="#">3</a></li>
        <li><a href="#">4</a></li>
        <li><a href="#">5</a></li>
        <li><a href="#"><span aria-hidden="true">»</span><span class="sr-only">Next</span></a></li>
     </ul>
   </nav>
 <!--table-->

 <div class="panel panel-default">
  <!-- Default panel contents -->
  <div class="panel-heading"><strong>Customer Detail</strong></div>


  <!-- Table -->
   <div class="container">  

    <table class="table table-bordered" action="/show_customerdetail">
    <thread>
        <tr>
          <th>Select</th>
          <th>Customer ID</th>
          <th>Customer Name</th>
          <th>Email</th>
        </tr>
    </thread>    
        %for row in rows:
    <tr>
    %for col in row:
        <td><input type="checkbox" value="">{{col}}</td>
    %end
    </tr>
%end
<!--
</table>       
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Select</th>
          <th>Customer ID</th>
          <th>Customer Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><input type="checkbox" value=""></td>
          <td>1</td>
          <td>John</td>
          <td>john@example.com</td>
        </tr>


      </tbody>
    </table>
    -->
  </div>
</div>
 <!--pager-->
     <div class="container">
      <ul class="pager">
        <li class="previous"><a href="">Previous</a></li>
        <li><button type="button" class="btn btn-primary">Update</button></li>
        <li><button type="button" class="btn btn-info">Delete</button></li>
        <li class="next"><a href="">Next</a></li>
      </ul>
    </div>
  </div>







    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>