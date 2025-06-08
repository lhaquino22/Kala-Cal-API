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
  #form1 table tbody tr td label strong {
	color: #F00;
}
#form1 table tbody tr td strong label {
	color: #F00;
}
</style>
</head>



<body>

<center>
<table align="center" border="0" width="55%">

  <tbody>

    <tr>

      <td>
      <center><img src="imagens/prevent.png" height="83" width="100%" /></center>

      </td>

    </tr>

    <tr bgcolor="#99ffcc">

      <td class="titulo" bgcolor="#cccccc"><span style="background-color: rgb(201, 201, 201);">PROGNOSTICATING KALA-AZAR</span></td>

    </tr>

    <tr bgcolor="#ffffff">

      <td class="subtitulo">Modelo Clinic and <span id="realce">laboratorial <span style="color: rgb(51, 51, 255);">model</span></span>,
age range: <? echo $faixaEtaria?> (<a href="index.php">switch</a>)</td>

    </tr>

    <tr>

      <td><form id="form1" name="form1" method="post" onsubmit="return enviardados()" action=<? echo '"resultado_adult_clinic_lab.php?id='.$id.'"'?>>
        <table align="center" border="0" cellpadding="1" cellspacing="1" width="80%">

          <tbody>

            <tr>

              <td width="40%">&nbsp;</td>

              <td width="60%">&nbsp;</td>

            </tr>

            <tr>

              <td class="campos" bgcolor="#cccccc">Number
of bleeding sites:</td>

              <td class="campos" bgcolor="#cccccc">Other
signs and symptoms:</td>

            </tr>

            <tr>

              <td bgcolor="#e9e9e9" valign="top"><label>
              <input name="sangramento" value="1" id="sitiosdesangramento_0" type="radio" /> None</label>
              <br />

              <label> <input name="sangramento" value="2" id="sitiosdesangramento_1" type="radio" />1
to 2 sites</label> <br />

              <label> <input name="sangramento" value="3" id="sitiosdesangramento_2" type="radio" />3
to 5 sites</label> <br />

              <label> <input name="sangramento" value="4" id="sitiosdesangramento_3" type="radio" />5
to 6 sites</label></td>

              <td rowspan="3" bgcolor="#e9e9e9" valign="top"> <label> <input name="clinicos[]" value="aids" id="sinaisesintomas_1" type="checkbox" />
HIV/AIDS</label> <br />

              <label> <input name="clinicos[]" value="ictericia" id="sinaisesintomas_2" type="checkbox" />
Jaundice</label> <br />

              <label> <input name="clinicos[]" value="dispneia" id="sinaisesintomas_3" type="checkbox" />
Dyspnoea</label> <br />

              <label> <input name="clinicos[]" value="infeccao" id="sinaisesintomas_4" type="checkbox" />
Bacterial infection</label> <br />

              <label> <input name="clinicos[]" value="leucopenia" id="sinaisesintomas_5" type="checkbox" />
                <strong>Leukocytes &lt; 1500/mm3</strong></label> 
              <strong><br />

              <label> <input name="clinicos[]" value="plaquetopenia" id="sinaisesintomas_6" type="checkbox" /> Platelets &lt; 50000</label> 
              <br />

              <label> <input name="clinicos[]" value="insuficienciaRenal" id="sinaisesintomas_7" type="checkbox" /> Kidney failure</label>
              <br />

              </strong></td>

            </tr>

            <tr>

              <td valign="top">&nbsp;</td>

            </tr>

            <tr>

              <td valign="top">&nbsp;</td>

            </tr>

            <tr>

              <td><br />

              </td>

              <td valign="top">&nbsp;</td>

            </tr>

            <tr>

              <td colspan="2">
              <center> <input src="imagens/cancelar.jpg" align="center" height="104" type="image" width="104" /> &nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp; <input src="imagens/ok.jpg" align="center" height="104" type="image" width="104" /> </center>

              </td>

            </tr>

          </tbody>
        </table>

      </form>

      </td>

    </tr>

    <tr>

      <td>&nbsp;</td>

    </tr>

  </tbody>
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
  
   
   //verifica se marcou sangramento.
   if((!document.form1.sitiosdesangramento_0.checked) && (!document.form1.sitiosdesangramento_1.checked) && (!document.form1.sitiosdesangramento_2.checked) && (!document.form1.sitiosdesangramento_3.checked)) {
	   alert("Please choose at least one option for number of bleeding sites");
	   return false;
   }
   
    if((!document.form1.sinaisesintomas_5.checked) || (!document.form1.sinaisesintomas_6.checked) || (!document.form1.sinaisesintomas_7.checked)) {
	   alert("Error: In this model we need all laboratory criteria(red) are met to proceed. Please use the clinical model!" ); 
	   return false;
   }
   
return true; 
} 
</script>
