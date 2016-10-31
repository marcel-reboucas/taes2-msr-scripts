#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>


char * internal_tok;
int nextStart=0;
char * nxtToken(char * inp,char delim, char quote,bool cont){
	int tam = strlen(inp);
	int start=0,end=tam;
	bool hasQuote=false;
	bool quoteReached=false;
	if(!cont)
		nextStart=0;

	for(int i = nextStart; i < tam; i++){
		if(inp[i]!=' '){
			hasQuote=inp[i]==quote;
			start=i;
			break;
		}
	}

	if(hasQuote){
		for(int i = start+1; i<tam;i++){
			if(inp[i]==quote){
				end=i;
				break;
			}
		}
		nextStart=end;
		while(inp[nextStart]!=',' && inp[nextStart]!='\0')
			nextStart++;
		nextStart++; 
	} else {
		for(int i = start+1; i<tam;i++){
			if(inp[i]==delim || inp[i]=='\0'){
				nextStart=i+1;
				end=i-1;
				while(inp[end]==' ')
					end--;
				break;
			}
		}

	}
	//printf("nextStart:%d start:%d end:%d\n",nextStart,start,end);
	memcpy(internal_tok,inp+start,(end-start+1)*sizeof(char));
	internal_tok[end-start+1]='\0';
	//printf("Lido:%s\n",internal_tok);
	return internal_tok;
}


char * emptyStr="\0";
struct estring {
	char str[1000];
	estring(char * pt){
		strcpy(str,pt);
	}
	bool operator< (const estring& lhs) const {
		return strcmp(str,lhs.str)<0;
	}
};

struct line {
	char projectName[1000];
	char commiterName[200];
	char commiterEmail[200];
	int numOfSuccessfullBuilds;
	int numOfFailedBuilds;
	int totalNumOfBuilds;
	int isCasual;
	
	void clear(){
		numOfSuccessfullBuilds=0;
		numOfFailedBuilds=0;
		totalNumOfBuilds=0;
	}
	line(const line& other){
		strcpy(projectName,other.projectName);
		strcpy(commiterName,other.commiterName);
		strcpy(commiterEmail,other.commiterEmail);
		numOfSuccessfullBuilds=other.numOfSuccessfullBuilds;
		numOfFailedBuilds=other.numOfFailedBuilds;
		totalNumOfBuilds=other.totalNumOfBuilds;
		isCasual=other.isCasual;

	}	

	line(char * inProjectName=emptyStr, char *inCommiterName=emptyStr, char * inCommiterEmail=emptyStr,int inNumOfSuccessfullBuilds=0, 
		int inNumOfFailedBuilds=0,int inTotalNumOfBuilds=0, int inIsCasual=0){
		strcpy(projectName,inProjectName);
		strcpy(commiterName,inCommiterName);
		strcpy(commiterEmail,inCommiterEmail);
		numOfSuccessfullBuilds=inNumOfSuccessfullBuilds;
		numOfFailedBuilds=inNumOfFailedBuilds;
		totalNumOfBuilds=inTotalNumOfBuilds;
		isCasual=inIsCasual;
	}
};


int main(){
	std::map<estring, std::map<estring,line> > output;
	FILE * in = fopen("output.csv","r");
	FILE * sumario = fopen("out_summary.csv","w+");
	char linha[1000000];
	char status[1000];
	int success;
	int lineNum=1;
	char * delim = ",\n";
	char * token;
	line act;
	internal_tok = (char*)malloc(500000*sizeof(char));
	if(in!=NULL){
		printf("Leitura do arquivo iniciada!\n");
		fgets(linha,1000000,in);//cabecalho
		while(fgets(linha,1000000,in)!=NULL){
			act.clear();
                        token = nxtToken(linha,',','\"',false);
                        token = nxtToken(linha,',','\"',true);
                        token = nxtToken(linha,',','\"',true);
			strcpy(act.projectName,token);
			
                        token = nxtToken(linha,',','\"',true);
			strcpy(act.commiterName,token);
			
			strcpy(output[act.projectName][act.commiterName].projectName,act.projectName);
			strcpy(output[act.projectName][act.commiterName].commiterName,act.commiterName);

                        token = nxtToken(linha,',','\"',true);
			strcpy(output[act.projectName][act.commiterName].commiterEmail,token);

                        token = nxtToken(linha,',','\"',true);
			strcpy(status,token);

			success=strcmp(status,"\"passed\"")==0?1:0;
			output[act.projectName][act.commiterName].numOfSuccessfullBuilds+=success;
			output[act.projectName][act.commiterName].numOfFailedBuilds+=!success;
			output[act.projectName][act.commiterName].totalNumOfBuilds++;
			output[act.projectName][act.commiterName].isCasual=output[act.projectName][act.commiterName].totalNumOfBuilds<10;
			//output[act.projectName][act.commiterName]=act;
			//printf("Linha processada: %d\n",lineNum);
			lineNum++;
		}
		printf("Fim da leitura do arquivo!\n");
		printf("Teste\nProjeto:%s\nNome:%s\nEmail:%s\nSucessos:%d\nFalhas:%d\nTotal:%d\n",
			output["\"47deg/appsly-android-rest\""]["\"Raúl Raja Martínez\""].projectName,
			output["\"47deg/appsly-android-rest\""]["\"Raúl Raja Martínez\""].commiterName,
			output["\"47deg/appsly-android-rest\""]["\"Raúl Raja Martínez\""].commiterEmail,
			output["\"47deg/appsly-android-rest\""]["\"Raúl Raja Martínez\""].numOfSuccessfullBuilds,
			output["\"47deg/appsly-android-rest\""]["\"Raúl Raja Martínez\""].numOfFailedBuilds,
			output["\"47deg/appsly-android-rest\""]["\"Raúl Raja Martínez\""].totalNumOfBuilds);

		fclose(in);
		printf("Iniciando escrita do resultado\n");
		fprintf(sumario,"\"Projeto\",\"Nome\",\"Email\",\"Sucessos\",\"Falhas\",\"Total\",\"Perc. sucesso\",\"Casual?\"\n");//cabecalho
		for(std::map<estring ,std::map<estring, line> >::iterator it=output.begin(); it!=output.end(); ++it){
			for(std::map<estring, line>::iterator it2=it->second.begin(); it2!=it->second.end(); ++it2){
				fprintf(sumario,"%s,%s,%s,%d,%d,%d,%.2f,\"%s\"\n",
					it2->second.projectName,
					it2->second.commiterName,
					it2->second.commiterEmail,
					it2->second.numOfSuccessfullBuilds,
					it2->second.numOfFailedBuilds,
					it2->second.totalNumOfBuilds,
					it2->second.numOfSuccessfullBuilds/(float)it2->second.totalNumOfBuilds,
					it2->second.isCasual?"Sim":"Não");
			}
		}

	} else {
		printf("Erro ao abrir arquivo de entrada!\n");
	}


	return 0;
}
