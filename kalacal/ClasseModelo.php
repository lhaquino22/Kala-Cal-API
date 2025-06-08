<?php

class ClasseModelo{

   private function limiteCasasDecimais($numeroDeCasas,$numero){
	     return number_format($numero, $numeroDeCasas, '.', '');
   }
 
   // Idade > 2 anos - Modelo Clínico (teste ok)
   public function probMorteMaior2anosClinico($escore){
	    $temp = 0.0;
        /*$x_in = $escore;

   	    $a1 = 5.8148354916182760E-04;
        $b1 = 5.6801343750080573E+00;
        $c1 = 5.1562506047888876E-07;
        $a2 = -7.4233868664717392E+01;
        $b2 = 4.7785915016481589E+01;
        $c2 = 4.0128022622005668E+00;
        $a3 = 1.0083877774712562E+00;
        $b3 = 7.1038583899577494E+00;
        $c3 = 1.2544042090323462E+00;


        $temp = $a1 / (1.0 + exp(-1.0 * ($x_in - $b1) / $c1)) + $a2 / (1.0 + exp(-1.0 * ($x_in - $b2) / $c2)) + $a3 / (1.0 + exp(-1.0 * ($x_in - $b3) /$c3)); */
        switch($escore){
            case 0: $temp = 0.003338385;break;
            case 1: $temp = 0.007394025;break;
            case 2: $temp = 0.016296045;break;
            case 3: $temp = 0.035531694;break;
            case 4: $temp = 0.075723719;break;
            case 5: $temp = 0.154109282;break;
            case 6: $temp = 0.288305571;break;
            case 7: $temp = 0.47384157;break;
            case 8: $temp = 0.666793942;break; 
            case 9: $temp = 0.816254194;break;
            case 10: $temp = 0.907745889;break; //estimada
            case 11: $temp = 0.955925539;break;
			case 12: $temp = 0.979297619;break; //estimada
			case 13: $temp = 0.9901837219;break; //estimada
        }
        return $this->limiteCasasDecimais(3,$temp);
	
   }
   
   // Idade > 2 anos - Modelo Clínico e Laboratorial (teste ok)
  public function probMorteMaior2anosClinicoElaboratorial($escore)
{
        $temp = 0.0;
        /*$x_in = $escore;
    
        // coefficients
		$a = 2.3143776698263655E+03;
		$b = 5.0961196614199258E+02;
		$c = -2.9631015829675584E+02;
		$d = 3.6003753679244433E+01;
		$f = 1.6617501464400963E+01;
		$g = -3.8303241650508486E+00;
		$h = 1.5949220887557849E+00;
		$Offset = 3.0000000000000543E-03;
		$temp += ($a + $b * $x_in + $c * $x_in * $x_in + $d * $x_in * $x_in * $x_in) / (1.0 + $f * $x_in + $g * $x_in *
$x_in + $h * $x_in * $x_in * $x_in);
		$temp = $x_in / $temp + $Offset;*/
		switch($escore){
            case 0: $temp = 0.000296031;break;
            case 1: $temp = 0.002497884;break;
            case 2: $temp = 0.016670987;break;
            case 3: $temp = 0.07829276;break;
            case 4: $temp = 0.239717557;break;
            case 5: $temp = 0.488427303;break;
            case 6: $temp = 0.732603013;break;
            case 7: $temp = 0.907305187;break;
			case 8: $temp = 1.010570531;break;
            case 9: $temp = 1.065581353;break;
            case 10: $temp = 1.093365948;break;
        }

		return $this->limiteCasasDecimais(3,$temp);
}

   // Idade < 2 anos - Modelo Clínico (teste ok)
  public function probMorteMenor2anosClinico($escore)
{   
      
        //Cálculo via ferramenta zumzum
		/*$x_in = $escore;
		$temp = 0.0;
		// coefficients
		$a = 1.6666666666666646E+02;
		$b = -5.4152415748057031E+01;
		$c = 6.2396513192125198E+00;
		$d = -2.7878422714130970E-02;
		$f = 1.1046591293044525E+00;
		$g = 7.4816709395861006E-02;
		$h = 1.9504463760183938E-01;
		$temp += ($a + $b * $x_in + $c * $x_in * $x_in + $d * $x_in * $x_in * $x_in) / (1.0 + $f * $x_in + $g * $x_in *
$x_in + $h * $x_in * $x_in * $x_in);
		$temp = 1.0 / $temp;
		*/
        $temp = 0.0;
        switch($escore){
            case 0: $temp = 0.000966832;break;
            case 1: $temp = 0.011300207;break;
            case 2: $temp = 0.030329499;break;
            case 3: $temp = 0.064934076;break;
            case 4: $temp = 0.127411596;break;
            case 5: $temp = 0.239744118;break;
            case 6: $temp = 0.441223098;break;
            case 7: $temp = 0.802077796;break;
            case 8: $temp = 1.447833833;break;
            case 9: $temp = 2.602850084;break;
        }
		
       return $this->limiteCasasDecimais(3,$temp);
}

    // Idade < 2 anos - Modelo Clínico e Laboratorial (teste ok)
 public function probMorteMenor2anosClinicoElaboratorial($escore)
{
		/*$x_in = $escore;
		$temp = 0.0;
		// coefficients
		$a = -2.8227307514176261E-02;
		$b = 4.2365104976892880E+00;
		$c = -2.3557119837563731E-01;
		$d = 3.9646856861752946E+00;
		$f = 2.3093003780221149E+00;
		$g = -9.4915888417824590E-01;
		$h = 2.7244054648491250E-01;
		$i = 4.5977454824049371E+00;
		$Offset = 9.9641971416188069E-01;
		$temp = $a * exp(-$b * $x_in) + $c * exp(-1.0 * ($x_in-$d) * ($x_in-$d) / ($f * $f)) + $g * exp(-1.0 * ($x_in
-$h) * ($x_in-$h) / ($i * $i));
		$temp += $Offset;*/
        $temp = 0.0;
        switch($escore){
            case 0: $temp = 0.001228266;break;
            case 1: $temp = 0.003789667;break;
            case 2: $temp = 0.011090773;break;
            case 3: $temp = 0.030042234;break;
            case 4: $temp = 0.073187025;break;
            case 5: $temp = 0.156050276;break;
            case 6: $temp = 0.286334983;break;
            case 7: $temp = 0.45223825;break;
            case 8: $temp = 0.62553836;break; 
            case 9: $temp = 0.778752936;break;
            case 10: $temp = 0.897964538;break;
			case 11: $temp = 0.982676514;break;
        }
		return $this->limiteCasasDecimais(3,$temp);
}
   
   
}


?>

