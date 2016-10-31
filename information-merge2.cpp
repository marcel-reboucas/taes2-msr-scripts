#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>

struct commiter_info {
	char nome[100];
	char email[100];
};

struct nova_linha {
	int row;
	char nome[100];
	char email[100];
	char status[12];
	char nomeprojeto[1000];
};

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

int main () {
        char linha[1100000];
	int* apontador_row;
	std::map<int,int> map_build_committer;
        commiter_info* committers;
	int ctnCommitters=0;
	int qtdLinhasTravis=0;
	int row;
	int build_id;
	char build_id_str[1000];
        char * p_token;
        FILE * in2 = fopen("/home/marcel/msr/travistorrent-5-3-2016-2.csv","r");
        FILE * in = fopen("/home/marcel/msr/build-commiter-info-threaded.csv","r");
	FILE * output = fopen("output.csv","w+");
	internal_tok = (char*)malloc(500000*sizeof(char));
	apontador_row = (int*)malloc(3000000*sizeof(int));
	memset(apontador_row,-1,3000000*sizeof(int));
	committers = (commiter_info*)malloc(3000000*sizeof(commiter_info));

        if(in != NULL){
		printf("Leitura do arquivo de informacoes de committers iniciada!\n");
		fgets(linha,10000,in);//avancando cabecalho
        	while(fgets(linha,10000,in)!=NULL){
                        p_token = nxtToken(linha,',','\"',false);
			row=atoi(p_token);
			//printf("Passou\n");
                        p_token = nxtToken(linha,',','\"',true);
			
			//printf("Passou2\n");
			/*strcpy(build_id_str,p_token);
			build_id_str[strlen(build_id_str)-1]='\0';
			build_id=atoi(build_id_str+1);*/
			build_id=atoi(p_token);

                        p_token = nxtToken(linha,',','\"',true);
			//printf("Passou3\n");
        		if(p_token!=NULL){
				apontador_row[row]=ctnCommitters;
				map_build_committer[build_id]=ctnCommitters;
				strcpy(committers[ctnCommitters].nome,p_token);	
				p_token = nxtToken(linha,',','\"',true);
				strcpy(committers[ctnCommitters].email,p_token);	
				
				if(committers[ctnCommitters].email[strlen(p_token)-1]=='\n')
					committers[ctnCommitters].email[strlen(p_token)-1]='\0';//rmovendo quebra de linha

				ctnCommitters++;
			}
			else
				printf("Nulo!\n");
        	}
		printf("Fim da leitura do arquivo de informacoes de committers. %d linhas lidas\n",ctnCommitters);
        } else {
		printf("Nao consegui abrir o arquivo das informacoes dos committers!\n");
	}
	fclose(in);

	
	nova_linha outputLine;
	if(in2 != NULL){
		printf("Leitura do arquivo do travis iniciada!\n");
                fgets(linha,1100000,in2);//avancando cabecalho
                while(fgets(linha,1100000,in2)!=NULL){
			fflush(in2);
                        p_token = nxtToken(linha,',','\"',false);
                        row=atoi(p_token);outputLine.row=row;
                        p_token = nxtToken(linha,',','\"',true);
                        p_token = nxtToken(linha,',','\"',true);
			strcpy(outputLine.nomeprojeto,p_token);

			for(int i = 0 ; i < 29; i++)
				p_token = nxtToken(linha,',','\"',true);
                        build_id=atoi(p_token);

                        p_token = nxtToken(linha,',','\"',true);
                        p_token = nxtToken(linha,',','\"',true);
			strcpy(outputLine.status,p_token);

			fprintf(output,"%d,%d,%s,%s,%s,%s\n",outputLine.row,build_id,outputLine.nomeprojeto,
                                committers[map_build_committer[build_id]].nome,
                                committers[map_build_committer[build_id]].email,
				outputLine.status);


			qtdLinhasTravis++;
			fflush(output);
                }
		printf("Fim da leitura do arquivo travis. %d linhas lidas\n",qtdLinhasTravis);
        } else {
                printf("Nao consegui abrir o arquivo do travis!\n");
        }
	fclose(in2);
	fclose(output);
	printf("Linhas no arquivo do travis: %d\n",qtdLinhasTravis);


	

        return 0;
}

