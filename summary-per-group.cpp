#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <math.h>
extern char* internal_tok;
char * nxtToken(char * inp,char delim, char quote,bool cont);

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

struct lineIn{
	char projectName[1000];
	int isCasual;
	int success;
	int failure;
	int total;
};

struct lineOut {
	int numOfContributors;
	int numOfCasual;
	int numOfNonCasual;
	int numOfCasualSuccess;
	int numOfCasualBuilds;
	int numOfNonCasualSuccess;
	int numOfNonCasualBuilds;

};

#define READ_SIZE 1000000
int main (){
	std::map<estring, lineOut > output;
	internal_tok = (char*)malloc(500000*sizeof(char));
	FILE * in = fopen("out_summary.csv","r");
	FILE * sumario = fopen("group-summary.csv","w+");
	char linha[READ_SIZE];
	lineOut actOut;
	lineIn actIn;
	char * token; 
	int lineCount=1;
	if(in!=NULL){
		printf("Leitura do arquivo iniciada!\n");
		fgets(linha,READ_SIZE,in);//cabecalho
		while(fgets(linha,READ_SIZE,in)!=NULL){
                        token = nxtToken(linha,',','\"',false);
			strcpy(actIn.projectName,token);
			
                        token = nxtToken(linha,',','\"',true);
                        token = nxtToken(linha,',','\"',true);

                        token = nxtToken(linha,',','\"',true);
			actIn.success=atoi(token);
                        token = nxtToken(linha,',','\"',true);
			actIn.failure=atoi(token);
                        token = nxtToken(linha,',','\"',true);
			actIn.total=atoi(token);

                        token = nxtToken(linha,',','\"',true);

                        token = nxtToken(linha,',','\"',true);
			actIn.isCasual = strcmp(token,"\"Sim\"")==0?1:0;
		
				
			output[actIn.projectName].numOfContributors++;
			if(actIn.isCasual){
				output[actIn.projectName].numOfCasual++;
				output[actIn.projectName].numOfCasualSuccess+=actIn.success;
				output[actIn.projectName].numOfCasualBuilds+=actIn.success+actIn.failure;
			} else {
				output[actIn.projectName].numOfNonCasual++;
				output[actIn.projectName].numOfNonCasualSuccess+=actIn.success;
				output[actIn.projectName].numOfNonCasualBuilds+=actIn.success+actIn.failure;
			}
			
			lineCount++;
		}
		printf("%d linhas lidas\n",lineCount);
		fclose(in);	
		printf("Escrita iniciada!\n");
		float percSuccCasual;
		float percSuccNonCasual;
		fprintf(sumario,"\"Projeto\",\"Qtd builds casuais\",\"Qtd builds não casuais\",\"Perc. sucesso casual\",\"Perc. sucesso não casual\",\"Quem ganha?\"\n");
		for(std::map<estring, lineOut>::iterator it=output.begin(); it!=output.end(); ++it) {
			percSuccCasual=it->second.numOfCasualBuilds!=0?it->second.numOfCasualSuccess/(float)it->second.numOfCasualBuilds:0;
			percSuccNonCasual=it->second.numOfNonCasualBuilds!=0?it->second.numOfNonCasualSuccess/(float)it->second.numOfNonCasualBuilds:0;
			fprintf(sumario,"%s,%d,%d,%.2f,%.2f,\"%s\"\n",
				it->first.str,it->second.numOfCasualBuilds,it->second.numOfNonCasualBuilds,
				percSuccCasual,percSuccNonCasual,percSuccCasual>percSuccNonCasual?"Casual":fabs(percSuccCasual-percSuccNonCasual)<0.001f?"Empate":"Não casual");
			
		}
		printf("Escrita terminada!\n");
		fclose(sumario);
	}	



	return 0;
}
