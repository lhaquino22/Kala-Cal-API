<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>

 <?php function redireciona($link){

if ($link==-1){

echo" <script>history.go(-1);</script>";

}else{

echo" <script>document.location.href='$link'</script>";

}

}

//clicou em modelo clínico

if (isset($_POST["bt_clinico"]) && isset($_POST["idade"])){

   $idade = $_POST["idade"];

   if($idade <=2) redireciona('child_clinic.php?id='.$_POST["idade"]); // pagina de criança modelo clínico 

   else redireciona('adult_clinic.php?id='.$_POST["idade"]); // pagina de adulto modelo clínico  

   
}



//clicou em modelo laboratorial

if (isset($_POST["bt_laboratorial"])&& isset($_POST["idade"])) {

   $idade = $_POST["idade"];

   
    //se criança.. chama página de criança

    if($idade <=2) redireciona('child_lab.php?id='.$_POST["idade"]);  // modelo clínico 

	 else redireciona('adult_lab.php?id='.$_POST["idade"]);

}

?>
 
  
  
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>DEATH PROBABILITY CALCULATION IN PATIENT WITH KALA-AZAR</title>


  <style type="text/css">
negrito {
font-weight: bold;
}
  .destac {
	color: #F00;
}
  #form1 table tbody tr td center p strong {
	color: #F00;
}
  </style>
</head>



<body>

<center>
<div style="text-align: center;">
</div>
<table style="width: 50%; text-align: left; margin-left: auto; margin-right: auto;" border="0">

  <tbody>

    <tr>

      <td>
      <div style="text-align: center;">
      <center><img src="imagens/prevent.png" height="83" width="489" /></center>
      </div>

      </td>

    </tr>

    <tr style="font-weight: bold;" align="center">
      <td style="background-color: rgb(201, 201, 201);">PROGNOSTICATING KALA-AZAR</td>
    </tr>
    <tr>

      <td>
      <form id="form1" name="form1" method="post" action="index.php">
        <table style="text-align: left; margin-left: auto; margin-right: auto; width: 80%;" border="0" cellpadding="1" cellspacing="1">

          <tbody>

            <tr>
              <td colspan="2"><p align="center"><strong>Estimation of the probability of death of persons with kala-azar  accordingly to data collected from patients treated in Teresina-PI, Brazil,  2005 - 2013.</strong></p></td>
              </tr>
            <tr>

              <td><br />

              </td>

              <td></td>

            </tr>

            <tr>

              <td style="width: 39%; background-color: rgb(204, 204, 204); font-weight: bold;">Age
range:</td>

              <td style="background-color: rgb(204, 204, 204); font-weight: bold;">Pick
the model:</td>

            </tr>

            <tr>

              <td style="vertical-align: top; background-color: rgb(233, 233, 233);">
              <label> <input name="idade" value="1" id="idade1" type="radio" /> &lt; 12 months old</label>
              <br />

              <label> <input name="idade" value="2" id="idade_1" type="radio" /> 12 - 23 months old</label>
              <br />

              <label> <input name="idade" value="3" id="idade_2" type="radio" /> 2-15 years old</label>
              <br />

              <label> <input name="idade" value="4" id="idade_3" type="radio" /> 16-39 years old</label>
              <br />

              <label> <input name="idade" value="5" id="idade_4" type="radio" /> &gt;40 years old</label>
              <br />

              </td>
              <td rowspan="1" style="vertical-align: top; background-color: rgb(233, 233, 233);">
              <p> <input name="bt_clinico" id="button" value="Use clinical model" type="submit" /> </p>
              <p> <input name="bt_laboratorial" id="button2" value="Use Clinical and Laboratorial model" type="submit" /> </p>

              </td>

            </tr>

            <tr>
              
              <td><br />
                
                </td>
              
            </tr>

            <tr>
              
              <td colspan="2">
                <center>
                  <img src="imagens/att.png" alt="att:" width="32" height="29" align="left" />
                  <p><strong>Warning:</strong> The estimations of probability of death should NOT be taken as a direct measurement  of the chance of dying of any particular patient, but rather as an indication of  disease severity of other similar patient population seen at different place or  time. </p>
<p align="justify">&nbsp;</p>
                </center>
                
                </td>
              
            </tr>

          </tbody>
        </table>

      </form>

      </td>

    </tr>

    <tr>

      <td style="text-align: center;">&nbsp;2016
Prevent&#174 All Rights Reservated - contact: <a href="mailto:eldochaves@gmail.com">eldochaves@gmail.com</a></td>

    </tr>

    <tr align="center">

      <td>&nbsp;</td>

    </tr>

  </tbody>
</table>

</center>

</body>
</html>
