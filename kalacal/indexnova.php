<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Documento sem título</title>
<style type="text/css">
negrito {
	font-weight: bold;
}
</style>
</head>

<body>
<center>
  <table width="50%" border="0" align="center">
    <tr>
      <td><center><img src="imagens/prevent.png" width="489" height="83" /></center></td>
    </tr>
    <tr>
      <td><form id="form1" name="form1" method="post" action="indexnova.php">
        <table width="80%" border="0" align="center" cellpadding="1" cellspacing="1">
          <tr>
            <td width="39%">Idade:</td>
            <td>Outros sinais e sintomas:</td>
            </tr>
          <tr>
            <td valign="top">
              <label>
                <input type="radio" name="idade" value="idade1" id="idade1" />
                < 12 meses</label>
              <br />
              <label>
                <input type="radio" name="idade" value="idade2" id="idade_1" />
                12 - 23 meses</label>
              <br />
              <label>
                <input type="radio" name="idade" value="idade3" id="idade_2" />
                2-20 anos</label>
              <br />
              <label>
                <input type="radio" name="idade" value="idade4" id="idade_3" />
                21-40 anos</label>
              <br />
              <label>
                <input type="radio" name="idade" value="idade5" id="idade_4" />
                >40 anos</label>
              <br />
             </td>
            <td rowspan="4" valign="top">
              <label>
                <input type="checkbox" name="clinicos" value="caixa de seleção" id="sinaisesintomas_0" />
                Edema</label>
              <br />
              <label>
                <input type="checkbox" name="clinicos" value="caixa de seleção" id="sinaisesintomas_1" />
                HIV/AIDS</label>
              <br />
              <label>
                <input type="checkbox" name="clinicos" value="caixa de seleção" id="sinaisesintomas_2" />
                Icterícia</label>
              <br />
              <label>
                <input type="checkbox" name="clinicos" value="caixa de seleção" id="sinaisesintomas_3" />
                Dispnéia</label>
              <br />
              <label>
                <input type="checkbox" name="clinicos" value="caixa de seleção" id="sinaisesintomas_4" />
                Infecção bacteriana</label>
              <br />
              <label>
                <input type="checkbox" name="lab" value="caixa de seleção" id="sinaisesintomas_5" />
                leucócitos < 1500/mm3</label>
              <br />
              <label>
                <input type="checkbox" name="lab" value="caixa de seleção" id="sinaisesintomas_6" />
                plaquetas < 50000</label>
              <br />
              <label>
                <input type="checkbox" name="lab" value="caixa de seleção" id="sinaisesintomas_7" />
                insuficiência renal</label>
              <br />
              <label>
                <input type="checkbox" name="lab" value="caixa de seleção" id="sinaisesintomas_8" />
                TGO ou TGP > 100 UK/L</label>
              <br />
            </p></td>
            </tr>
          <tr>
            <td>Sítios de sangramento:</td>
          </tr>
          <tr>
            <td valign="top"><label>
              <input type="radio" name="sangramento" value="nenhum" id="sitiosdesangramento_0" />
              nenhum</label>
              <br />
              <label>
                <input type="radio" name="sangramento" value="1a2" id="sitiosdesangramento_1" />
                1 a 2 sítios</label>
              <br />
              <label>
                <input type="radio" name="sangramento" value="3a5" id="sitiosdesangramento_2" />
                3 a 5 sítios</label>
              <br />
              <label>
                <input type="radio" name="sangramento" value="5a6" id="sitiosdesangramento_3" />
              5 a 6 sítios</label></td>
          </tr>
          <tr>
            <td><br />              </td>
          </tr>
          <tr>
            <td colspan="2"><center><input type="submit" name="calcular" id="calcular" value="Calcular" /></center></td>
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
