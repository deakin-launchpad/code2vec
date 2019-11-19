const example1 = `img_filename(const char *mapimgfile, enum imageformat format,
                         char *filename, size_t filename_len)
{
  fc_assert_ret_val(imageformat_is_valid(format) , FALSE);

  fc_snprintf(filename, filename_len, "%s.map.%s", mapimgfile,
              imageformat_name(format));

  return TRUE;
}`;


const example2 = `initLogFile(const unsigned int logLevel, const char* fileName, const char* fileMode)

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
`;


const example3 = `httpSetRoutePathVar(HttpRoute *route, cchar *key, cchar *value)

{

    mprAssert(route);

    mprAssert(key);

    mprAssert(value);

    GRADUATE_HASH(route, pathTokens);

    if (schr(value, '$')) {

        value = stemplate(value, route->pathTokens);

    }

    mprAddKey(route->pathTokens, key, sclone(value));

}`;

const example4 = `deallocate_pop (Population population)

{

  for (unsigned i = 0; i < population.length; i++)

    {               /* Remove population */

      free (population.person[i].summary.extra_shifts);

      free (population.person[i].summary.weekends_halved);

      free (population.person[i].summary.consecutive_weekends);

      free (population.person[i].summary.weekends);

      free (population.person[i].summary.freedays);

      delete[]population.person[i].summary.wrong_shifts;

      free (population.person[i].gene);

    }

  free (population.person);

}


wl3501_resume(struct pcmcia_device *link)

{

    struct net_device *dev = link->priv;

    wl3501_pwr_mgmt(netdev_priv(dev), WL3501_RESUME);

    if (link->open) {

        wl3501_reset(dev);

        netif_device_attach(dev);

    }

    return 0;

}`;
