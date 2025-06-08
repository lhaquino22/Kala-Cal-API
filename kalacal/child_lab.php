<?php
$id = $_GET['id'];
$faixaEtaria ='';

switch($id){
   case 1: $faixaEtaria = '< 12 years old';break; //não roda aqui
   case 2: $faixaEtaria = '12-23 years old';break; //não roda aqui
   case 3: $faixaEtaria = '2 - 15 years old';break;
   case 4: $faixaEtaria = '16 - 40 years old';break;
   case 5: $faixaEtaria = '> 40 years old';break;
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>DEATH PROBABILITY CALCULATION IN PATIENT WITH KALA-AZAR</title>
<style type="text/css">
negrito {
	font-weight: bold;
}
.titulo {
	font-size: 14px;
	text-align: center;
	font-weight: bold;
}
.subtítulo {
	font-size: 14px;
	text-align: left;
}
.subtitulo {
	text-align: left;
	font-size: 14;
	color: #00F;
	font-weight: bold;
}
.campos {
	font-weight: bold;
}
#realce {
	color: #F00;
	font-weight: bold;
}
lab_criteria {
	color: #F00;
}
#form1 table tr td label strong {
	color: #F00;
}
</style>
</head>

<body>
<center>
  <table width="55%" border="0" align="center">
    <tr>
      <td><center><img src="imagens/prevent.png" width="100%" height="83" /></center></td>
    </tr>
    <tr bgcolor="#99FFCC">
      <td bgcolor="#CCCCCC" class="titulo"><span style="background-color: rgb(201, 201, 201);">PROGNOSTICATING KALA-AZAR</span></td>
    </tr>
    <tr bgcolor="#FFFFFF">
      <td class="subtitulo">Clinical and <span id="realce"> laboratorial </span>model, age range: <? echo $faixaEtaria ?> (<a href="index.php">switch</a>)</td>
    </tr>
    <tr>
      <td><form id="form1" name="form1" method="post" onsubmit="return enviardados()" action=<? echo '"resultado_child_clinic_lab.php?id='.$id.'"'?>>
        <table width="80%" border="0" align="center" cellpadding="1" cellspacing="1">
          <tr>
            <td width="40%">&nbsp;</td>
            <td width="60%">&nbsp;</td>
          </tr>
          <tr>
            <td bgcolor="#CCCCCC" class="campos">Number of bleeding sites:</td>
            <td bgcolor="#CCCCCC" class="campos">Other signs and symptoms:</td>
            </tr>
          <tr>
            <td valign="top" bgcolor="#E9E9E9"><label>
              <input type="radio" name="sangramento" value="1" id="sitiosdesangramento_0" />
              None</label>
              <br />
              <label>
                <input type="radio" name="sangramento" value="2" id="sitiosdesangramento_1" />
                1 to 2 sites</label>
              <br />
              <label>
                <input type="radio" name="sangramento" value="3" id="sitiosdesangramento_2" />
                3 to 5 sites</label>
              <br />
              <label>
                <input type="radio" name="sangramento" value="4" id="sitiosdesangramento_3" />
                5 to 6 sítes</label></td>
            <td rowspan="3" valign="top" bgcolor="#E9E9E9">
              <label>
                <input type="checkbox" name="clinicos[]" value="edema" id="sinaisesintomas_0" />
                Edema</label>
              <br />
              <label>
                <input type="checkbox" name="clinicos[]" value="dispneia" id="sinaisesintomas_3" />
                Dyspnoea</label>
              <br />
              <label>
                <input type="checkbox" name="clinicos[]" value="hepatite" id="sinaisesintomas_8" / color="red">
                <strong>AST and ALT > 100 UK/L</strong></label>
              </p></td>
            </tr>
          <tr>
            <td valign="top">&nbsp;</td>
          </tr>
          <tr>
            <td valign="top">&nbsp;</td>
          </tr>
          <tr>
            <td colspan="2"><center>
              <input type="image" src="imagens/cancelar.jpg" align="middle" width="104" height="104" />
              &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;
              <input type="image" src="imagens/ok.jpg" align="middle" width="104" height="104" />
             
          </tr>
        </table>
      </form>
      </td>
    </tr>
    <tr>
      <td>&nbsp;</td>
    </tr>
  </table>
</center>

</body>
</html>
<?php
include("ClassePaciente.php");
include("ClasseModelo.php");
$quadro_clinico = null;
$sangramento = 0;
if(isset($_POST['sangramento'])){
    $sangramento = $_POST['sangramento'];
	if(isset($_POST['clinicos'])){
       $clinico = $_POST['clinicos'];
       foreach($clinico as $k => $v){
       $quadro_clinico[] = $v;
       }   
    }
	$paciente = new ClassePaciente();
	$paciente->processaFormulario($sangramento,$quadro_clinico,$id);
	$paciente->calcularEscoreLaboratorialAdulto();
	
	$modelo = new ClasseModelo(); 
	echo 'escore: '.$paciente->getEscore().'/10</p>';
	echo 'probabilidade de morte: '.$modelo->probMorteMaior2anosClinicoElaboratorial($paciente->getEscore()).'%';
}
?>

<script language="JavaScript" > 
function enviardados(){ 
  
  //verifica de dados laboratorias estão ok
  if(!document.form1.sinaisesintomas_8.checked) {
	   alert("Error: In this model we need all laboratory criteria are met to proceed. Please use the clinical model!" ); 
	   document.form1.sinaisesintomas_8.focus();
	   return false;
   }
   
   //verifica se marcou sangramento.
   if((!document.form1.sitiosdesangramento_0.checked) && (!document.form1.sitiosdesangramento_1.checked) && (!document.form1.sitiosdesangramento_2.checked) && (!document.form1.sitiosdesangramento_3.checked)) {
	   alert("Please choose at least one option for number of bleeding sites");
	   document.form1.sitiosdesangramento_0.defautckeck;
	   return false;
   }
   
return true; 
} 
</script>


