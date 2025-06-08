<?php

class ClassePaciente{
	
	private $escore=0;
	
	//Modelo
	private $clinico = false;
	private $clinicoElaboratorial = false;
	/*
	//faixa_etaria;
	private $idade_menor_12m = false;
	private $idade_12m_a_23m = false;
	private $idade_2a_20a = false;
	private $idade_21a_40a = false;
	private $idade_maior40a = false;*/
    
    private $idade_menor_12m = false;
	private $idade_12m_a_23m = false;
	private $idade_2a_15a = false;
	private $idade_16a_40a = false;
	private $idade_maior40a = false;
	
	//sangramentos
	private $sangram_nenhum = false;
	private $sangram_1a2 = false;
	private $sangram_3a4 = false;
	private $sangram_5a6 = false;
	
	
	//quadro clínico
	private $edema = false;
	private $aids = false;
	private $ictericia = false;
	private $dispneia = false;
	private $infeccao = false;
	private $leucopenia = false;
	private $plaquetopenia = false;
	private $insuficienciaRenal = false;
	private $hepatite = false;
	private $vomitos = false;

   public function setIdade($faixaEtaria){
		 switch($faixaEtaria){
   			case 1: $faixaEtaria = $this->idade_menor_12m = true;break;   //'< 12 meses';break; //não roda aqui
  		    case 2: $faixaEtaria = $this->idade_12m_a_23m = true;break;//'12-23 meses';break; //não roda aqui
            case 3: $faixaEtaria = $this->idade_2a_15a = true;break;//'2 - 15 anos';break;
            case 4: $faixaEtaria = $this->idade_16a_40a = true;break;//'16 - 40 anos';break;
            case 5: $faixaEtaria = $this->idade_maior40a = true;break;//'> 40 anos';break;
			}
   }
   
   public function setSangramento($numerositios){
		 switch($numerositios){
   			case 1: $numerositios = $this->sangram_nenhum = true;break;   //'< 12 meses';break; //não roda aqui
  		    case 2: $numerositios = $this->sangram_1a2 = true;break;//'12-23 meses';break; //não roda aqui
            case 3: $numerositios = $this->sangram_3a4 = true;break;//'2 - 20 anos';break;
            case 4: $numerositios = $this->sangram_5a6 = true;break;//'21 - 40 anos';break
			}
   }
   
    public function setQuadroClinico($quadro){
	     if ($quadro =='edema') $this->edema = true;
		 if ($quadro =='aids') $this->aids = true;
		 if ($quadro =='ictericia') $this->ictericia = true;
		 if ($quadro =='dispneia') $this->dispneia = true;
		 if ($quadro =='infeccao') $this->infeccao = true;
		 if ($quadro =='leucopenia') $this->leucopenia = true;
		 if ($quadro =='plaquetopenia') $this->plaquetopenia = true;
		 if ($quadro =='insuficienciaRenal') $this->insuficienciaRenal = true;
		 if ($quadro =='hepatite') $this->hepatite = true;
		 if ($quadro =='vomitos') $this->vomitos = true;
   }
   
   
  
   private function isCrianca(){
        if ($this->idade_menor_12m) return true;
		if ($this->idade_12m_a_23m) return true;
   }
   
   private function isAdulto(){
        if (!$this->isCrianca()) return true;
   }
   
   public function getEscore(){
        return $this->escore;
   }
   
   //essa função prepara a classe Paciente apartir de formulário.
   public function processaFormulario($sitios_sangramento,$quadro_clinico,$idade){
		$sangramento = $sitios_sangramento;

        if($quadro_clinico != null){
            $clinico = $_POST['clinicos'];
            $k = 0;
            foreach($clinico as $k => $v){
            $quadro_clinico[] = $v;
			}
       }

       $this->setIdade($idade);
       $this->setSangramento($sangramento);

       $i = 0;

       if($quadro_clinico != null){
            while(each($quadro_clinico)){
            $this->setQuadroClinico($quadro_clinico[$i]);
            $i++;
            }
       }
    }
   
   public function calcularEscoreClinicoCrianca(){
	       $this->escore = 0;
		
	   	   if($this->idade_menor_12m) $this->escore= $this->escore + 1;
		   if($this->idade_12m_a_23m) $this->escore+=0;
		   
		   if($this->sangram_nenhum) $this->escore+=0;
		   if($this->sangram_1a2) $this->escore+=1;
		   if($this->sangram_3a4) $this->escore+=2;
		   if($this->sangram_5a6) $this->escore+=4;
		   
		   if($this->ictericia) $this->escore+=1;
		   if($this->dispneia) $this->escore+=1;
           if($this->edema) $this->escore+=2; // NOVA VERSÃO DA TABELA
		   
		   return $this->escore;
   }  
   
   public function calcularEscoreLaboratorialCrianca(){
	       $this->escore = 0;
		    
	   	   if($this->idade_menor_12m) $this->escore= $this->escore + 1; //considera idade nova versao
		   if($this->idade_12m_a_23m) $this->escore+=0;
		   
		   if($this->sangram_nenhum) $this->escore+=0;
		   if($this->sangram_1a2) $this->escore+=1;
		   if($this->sangram_3a4) $this->escore+=2;
		   if($this->sangram_5a6) $this->escore+=4;
		   
		  // if($this->ictericia) $this->escore+=1; não usa icterícia
		   if($this->dispneia) $this->escore+=1;
		   if($this->edema) $this->escore+=2; // NOVA VERSÃO DA TABELA
		   if($this->hepatite) $this->escore+=3; //exclusivo do laboratorial
		   
		   return $this->escore;
   }  
   
    public function calcularEscoreClinicoAdulto(){
	       $this->escore = 0;
		
	   	   if($this->idade_menor_12m) $this->escore==0;
		   if($this->idade_12m_a_23m) $this->escore+=0;
		   if($this->idade_2a_15a) $this->escore+=0;
		   if($this->idade_16a_40a) $this->escore+=2;
		   if($this->idade_maior40a) $this->escore+=3;
		   
		   if($this->sangram_nenhum) $this->escore+=0;
		   if($this->sangram_1a2) $this->escore+=0;
		   if($this->sangram_3a4) $this->escore+=0;
		   if($this->sangram_5a6) $this->escore+=3;
		   
		   if($this->aids) $this->escore+=2;
		   if($this->edema) $this->escore+=1;
		   if($this->ictericia) $this->escore+=1;
		   if($this->dispneia) $this->escore+=1;
		   if($this->infeccao) $this->escore+=1;
		    if($this->vomitos) $this->escore+=1;
		 
		   
		   return $this->escore;
   }  
   
     public function calcularEscoreLaboratorialAdulto(){
	       $this->escore = 0;
		    
		   //Idade não influencia por enquanto
	   	   if($this->idade_menor_12m) $this->escore==0;
		   if($this->idade_12m_a_23m) $this->escore+=0;
		   if($this->idade_2a_15a) $this->escore+=0;
		   if($this->idade_16a_40a) $this->escore+=0;
		   if($this->idade_maior40a) $this->escore+=0;
		   
		   //sítios de sangramento não influenciam por enquanto
		   if($this->sangram_nenhum) $this->escore+=0;
		   if($this->sangram_1a2) $this->escore+=0;
		   if($this->sangram_3a4) $this->escore+=0;
		   if($this->sangram_5a6) $this->escore+=0;
		   
		   
		   if($this->aids) $this->escore+=2;
		   if($this->edema) $this->escore+=0;
		   if($this->ictericia) $this->escore+=1;
		   if($this->dispneia) $this->escore+=1;
		   if($this->infeccao) $this->escore+=1;
		   if($this->vomitos) $this->escore+=0;
		   if($this->leucopenia) $this->escore+=1;
		   if($this->plaquetopenia) $this->escore+=2;
		   if($this->vomitos) $this->escore+=0;
		   if($this->insuficienciaRenal) $this->escore+=2;
		 
		   
		   return $this->escore;
   }  
   
   
}


?>

