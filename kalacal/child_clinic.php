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
      <td class="subtitulo" align="center">Clinic model, age range: <? echo $faixaEtaria ?> (<a href="index.php">switch</a>)</td>
    </tr>
    <tr>
      <td><form id="form1" name="form1" method="post" action=<? echo '"resultado_child_clinic.php?id='.$id.'"'?>>
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
              5 to 6 sites</label>              <br />              <br />              </td>
            <td rowspan="3" valign="top" bgcolor="#E9E9E9">
              <label>
                <input type="checkbox" name="clinicos[]" value="edema" id="sinaisesintomas_0" />
                Edema</label>
              <br />
              <label>
                <input type="checkbox" name="clinicos[]" value="ictericia" id="sinaisesintomas_2" />
                Jaundice</label>
              <br />
              <label>
                <input type="checkbox" name="clinicos[]" value="dispneia" id="sinaisesintomas_3" />
                Dyspnoea</label>
              <br />
              <br />
              </p></td>
          </tr>
          <tr>
            <td valign="top">&nbsp;</td>
            </tr>
          <tr>
            <td valign="top">&nbsp;</td>
          </tr>
          <tr>
            <td><br />              </td>
            <td valign="top">&nbsp;</td>
          </tr>
          <tr>
            <td colspan="2"><center>
              <input type="image" src="imagens/cancelar.jpg" align="middle" width="104" height="104" id="cancelar" />
              &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;
              <input type="image" src="imagens/ok.jpg" align="middle" width="104" height="104" id="calcular" name="calcular" />
             
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
/*
//processamento do formulário

if(isset($_POST['sangramento'])){

$sangramento = $_POST['sangramento'];
$clinico = $_POST['clinicos'];

$k = 0;
foreach($clinico as $k => $v){
	$quadro_clinico[] = $v;
}

echo $sangramento;

$i = 0;
while(each($quadro_clinico)){
echo $quadro_clinico[$i].'<p>';
$i++;
}

}
*/
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
	$paciente->calcularEscoreClinicoAdulto();
	
	$modelo = new ClasseModelo(); 
	echo 'escore: '.$paciente->getEscore().'/13</p>';
	echo 'probabilidade de morte: '.$modelo->probMorteMaior2anosClinico($paciente->getEscore()).'%';
}
?>
