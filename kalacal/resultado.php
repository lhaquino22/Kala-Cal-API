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
	text-align: left;
	font-size: 14;
	color: #00F;
	font-weight: bold;
}
.campos {
	color: #000;
	text-align: left;
	font-weight: normal;
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
      <td bgcolor="#CCCCCC" class="titulo">CÁLCULO DA PROBABILIDADE DE MORTE EM PACIENTE COM CALAZAR</td>
    </tr>
    <tr bgcolor="#FFFFFF">
      <td class="subtitulo">Modelo clínico, faixa etária: <? echo $faixaEtaria ?> (<a href="index.php">trocar</a>)</td>
    </tr>
    <tr>
      <td></td>
    </tr>
    <tr>
      <td class="subtitulo">Sítios de Sangramento: 1 a 2 sítios</td>
    </tr>
    <tr>
      <td class="subtitulo">Quadro Clínico: Edema, dispnéia, Icterícia</td>
    </tr>
    <tr>
      <td class="subtitulo">&nbsp;</td>
    </tr>
    <tr>
      <td class="subtitulo"><table width="50%" border="0" align="center" cellpadding="1" cellspacing="1">
        <tr bgcolor="#CCCCCC">
          <td class="campos" bgcolor="#999999">Resultados</td>
        </tr>
        <tr bgcolor="#CCCCCC">
          <td class="campos">Escore: 11/13 </td>
        </tr>
        <tr bgcolor="#CCCCCC">
          <td class="campos">Probabilidade de Morte: 59,0 %</td>
        </tr>
      </table></td>
    </tr>
    <tr>
      <td class="subtitulo"><img src="imagens/teste.jpg" width="673" height="408" /></td>
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
