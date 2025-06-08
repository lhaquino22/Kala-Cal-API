<?php
$id = $_GET['id'];
$faixaEtaria ='';

switch($id){
   case 1: $faixaEtaria = '< 12 meses';break; //não roda aqui
   case 2: $faixaEtaria = '12-23 meses';break; //não roda aqui
   case 3: $faixaEtaria = '2 - 20 anos';break;
   case 4: $faixaEtaria = '21 - 40 anos';break;
   case 5: $faixaEtaria = '> 40 anos';break;
}
?>
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
	$paciente->calcularEscoreClinicoCrianca();
	
	$modelo = new ClasseModelo(); 
	//echo 'escore: '.$paciente->getEscore().'/8</p>';
	//echo 'probabilidade de morte: '.$modelo->probMorteMenor2anosClinicoElaboratorial($paciente->getEscore()).'%';
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Documento sem título</title>
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
	text-align: center;
	font-size: 14;
	color: #00F;
	font-weight: bold;
}
.campos {
	color: #000;
	text-align: left;
	font-weight: normal;
}
.realce {
	color: #00C;
	font-weight: bold;
}
.titulo {
	font-size: large;
}
titulo2 {
	font-size: 24px;
}
.titulo1 {
	font-size: 16px;
	text-align: center;
	font-weight: bold;
}
.subtitulo1 {	text-align: left;
	font-size: 14;
	color: #00F;
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
      <td class="subtitulo"><span class="subtitulo1">Clinical model, age range:</span> <? echo $faixaEtaria ?> (<a href="index.php">switch</a>)</td>
    </tr>
    <tr>
      <td></td>
    </tr>
    <tr>
      <td class="subtitulo">&nbsp;</td>
    </tr>
    <tr>
      <td class="subtitulo"><span class="titulo">RESULT:</span></td>
    </tr>
    <tr>
      <td class="subtitulo"><table width="50%" border="0" align="center" cellpadding="1" cellspacing="1">
        <tr bgcolor="#CCCCCC">
          <td class="campos" bgcolor="#999999">Sumary:</td>
        </tr>
        <tr bgcolor="#CCCCCC">
          <td class="campos">Score: <span class="realce"><? echo $paciente->getEscore().'/9';?></span></td>
        </tr>
        <tr bgcolor="#CCCCCC">
          <td class="campos">Probability of death: <span class="realce"><? echo ($modelo->probMorteMenor2anosClinico($paciente->getEscore())*100).'%';?></span></td>
        </tr>
      </table></td>
    </tr>
    <tr>
      <td class="subtitulo"><img src="imagens/graf_child_clinic.jpg" width="673" height="408" /></td>
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
/*
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
?>*/
