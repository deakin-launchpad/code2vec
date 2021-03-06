/* 
// C extractor for code2vec
// Copyright 2019 Carnegie Mellon University. All Rights Reserved.
//
// NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
// Released under a MIT (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
// [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
// Carnegie Mellon® and CERT® are registered in the U.S. Patent and Trademark Office by Carnegie Mellon University.
// This Software includes and/or makes use of the following Third-Party Software subject to its own license:
// 1. code2vec (https://github.com/tech-srl/code2vec/blob/master/LICENSE) Copyright 2018 Technion.
// 2. LLVM / CLANG (https://github.com/llvm-mirror/clang/blob/master/LICENSE.TXT) Copyright 2019 LLVM.
// DM19-0540
*/

/*
int sum_square(int v1, int v2) {
	        return (v1+v2)*(v1+v2);
}

int foo(int n) {
	        if (n < 0) {
			                return -n;
					        }
		        return n;
}

int f(int n) {
	    if (n == 0) {
		            return 1;
			        } else {
					        return n * f(n-1);
						    }
}

abs2(int *v)
{
    if((*v) < 0) { (*v) = -(*v); }
}


last_name(void){
    char last_name[20];
    printf ("Enter your last name: ");
    scanf ("%s", last_name);
}
*/
LoadPersistentContext()

{ CF_DB *dbp;
  CF_DBC *dbcp;
  int ksize,vsize;
  char *key;
  void *value;
  time_t now = time(NULL);
  struct CfState q;
  char filename[CF_BUFSIZE];

if (LOOKUP)
  {
  return;
  }

Banner(""Loading persistent classes"");

snprintf(filename,CF_BUFSIZE,""%s/state/%s"",CFWORKDIR,CF_STATEDB_FILE);
MapName(filename);

if (!OpenDB(filename,&dbp))
   {
   return;
   }

/* Acquire a cursor for the database. */

if (!NewDBCursor(dbp,&dbcp))
   {
   CfOut(cf_inform,"""","" !! Unable to scan persistence cache"");
   return;
   }

while(NextDB(dbp,dbcp,&key,&ksize,&value,&vsize))
   {
   memcpy((void *)&q,value,sizeof(struct CfState));

   Debug("" - Found key %s...\n"",key);

   if (now > q.expires)
      {
      CfOut(cf_verbose,"""","" Persistent class %s expired\n"",key);
      DeleteDB(dbp,key);
      }
   else
      {
      CfOut(cf_verbose,"""","" Persistent class %s for %d more minutes\n"",key,(q.expires-now)/60);
      CfOut(cf_verbose,"""","" Adding persistent class %s to heap\n"",key);
      NewClass(key);
      }
   }

DeleteDBCursor(dbp,dbcp);
CloseDB(dbp);

Banner(""Loaded persistent memory"");
}