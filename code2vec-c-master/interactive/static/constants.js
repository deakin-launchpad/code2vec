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

const airbnb = `If your Country of Residence is the United States , the Data Controller is Airbnb , Inc . If your Country of Residence is outside of the United States , the People 's Republic of China which for purposes of this Privacy Policy does not include Hong Kong , Macau and Taiwan ( â€œ China â€ ) and Japan , the Data Controller is Airbnb Ireland UC ( â€œ Airbnb Ireland â€ ) . If you change your Country of Residence , the Data Controller and/or Payments Data Controller will be determined by your new Country of Residence as specified above , from the date on which your Country of Residence changes . To this end the Data Controller and/or Payment Data Controller that originally collected your personal information will need to transfer such personal information to the new applicable Data Controller and/or Payments Data Controller due to the fact that such transfer is necessary for the performance of the contractual relationship with you . To help create and maintain a trusted environment , we may collect identity verification information ( such as images of your government issued ID , passport , national ID card , or driving license , as permitted by applicable laws ) or other authentication information . `

const amazon = `Information You Give Us : we receive and store any information you provide in relation to Amazon Services .
Click here to see examples of what we collect .
You can choose not to provide certain information but then you might not be able to take advantage of many of our Amazon Services . We use your personal information to take and handle orders , deliver products and services , process payments , and communicate with you about orders , products and services , and promotional offers . We may also use scoring methods to assess and manage credit risks . We may also ask for your consent to process your personal information for a specific purpose that we communicate to you .`

const apple = `You may be asked to provide your personal information anytime you are in contact with Apple or an Apple affiliated company . Apple and its affiliates may share this personal information with each other and use it consistent with this Privacy Policy . Apple will use such information to fulfill your requests , provide the relevant product or service , or for anti-fraud purposes . The personal information we collect allows us to keep you posted on Apple 's latest product announcements , software updates , and upcoming events .
If you do not want to be on our mailing list , you can opt out anytime by updating your preferences .
We also use personal information to help us create , develop , operate , deliver , and improve our products , services , content and advertising , and for loss prevention and anti-fraud purposes .`

const facebook = `To provide the Facebook Products , we must process information about you . This can include information in or about the content you provide ( like metadata ) , such as the location of a photo or the date a file was created . Data with special protections : You can choose to provide information in your Facebook profile fields or Life Events about your religious views , political views , who you are " interested in , " or your health . Device signals : Bluetooth signals , and information about nearby Wi-Fi access points , beacons , and cell towers .`
