initLogFile(const unsigned int logLevel, const char* fileName, const char* fileMode)

{

   finishLogging();

   if(fileName != NULL) {

      *gStdLog = fopen(fileName,fileMode);

      if(*gStdLog != NULL) {

         gCloseStdLog = true;

         gLogLevel   = min(logLevel,MAX_LOGLEVEL);

         return(true);

      }

   }

   *gStdLog     = stderr;

   gCloseStdLog = false;

   return(false);

}

get_nth_ancestor(const char *name, int len,

                unsigned char *result, int generation)

{

    unsigned char sha1[20];

    int ret = get_sha1_1(name, len, sha1);

    if (ret)

        return ret;

    while (generation--) {

        struct commit *commit = lookup_commit_reference(sha1);

        if (!commit || parse_commit(commit) || !commit->parents)

            return -1;

        hashcpy(sha1, commit->parents->item->object.sha1);

    }

    hashcpy(result, sha1);

    return 0;

}
