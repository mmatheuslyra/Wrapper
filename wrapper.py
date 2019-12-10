import os
import json
from pprint import pprint

# import wrapper
# emb = wrapper.Embeddings()
# emb.setEnv('remote')
# emb.Word2vec()
# emb.Wang2vec()

class Embeddings:

    def __init__(self, env='local'):
        with open('environment/{}.json'.format(env)) as data_file:    
            self.data = json.load(data_file)

    def setEnv(self, env = 'local'):
        with open('environment/{}.json'.format(env)) as data_file:
            self.data = json.load(data_file)
        print('Environment set to:', env)    

    def putTrainFile(self):
        os.system("sshpass -p %s scp -r ../../../%s %s:./PLN/word2vec/trunk/data/%s"%(self.data["password"], self.data["train"], self.data["UserServer"], self.data["train"]))

    def Word2vec(self, train = None, output = None, cbow = None , size = None, window =  None, negative = None, hs = None, sample = None, threads = None, binary = None, iter = None, mincount = None, batchSize = None, local = None, user = None, UserServer = None, password = None, nodes = None, cluster = None, ppn = None, walltime = None, email = None):
        train = train if train != None else self.data["train"]
        output = output if output != None else self.data["output"]
        cbow = cbow if cbow != None else self.data["cbow"]
        size = size if size != None else self.data["size"]
        window =  window if window != None else self.data["window"]
        negative = negative if negative != None else self.data["negative"]
        hs = hs if hs != None else self.data["hs"]
        sample = sample if sample != None else self.data["sample"]
        threads = threads if threads != None else self.data["threads"]
        binary = binary if binary != None else self.data["binary"]
        iter = iter if iter != None else self.data["iter"]
        mincount = mincount if mincount != None else self.data["mincount"]
        batchSize = batchSize if batchSize != None else self.data["batch-size"]
        local = local if local != None else self.data["local"]
        user = user if user != None else self.data["user"]
        UserServer = UserServer if UserServer != None else self.data["UserServer"]
        password = password if password != None else self.data["password"]
        nodes = nodes if nodes != None else self.data["nodes"]
        cluster = cluster if cluster != None else self.data["cluster"]
        ppn = ppn if ppn != None else self.data["ppn"]
        walltime = walltime if walltime != None else self.data["walltime"]
        email = email if email != None else self.data["email"]
        os.system("chmod +x word2vec.sh")
        os.system("./word2vec.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%(train, output, cbow, size, window, negative, hs, sample, threads, binary, iter, mincount, local, user, UserServer, password, nodes, cluster, ppn, walltime, email))

    #verificar compilador na pantanal    
    def pWord2vec(self, train = None, output = None, cbow = None , size = None, window =  None, negative = None, hs = None, sample = None, threads = None, binary = None, iter = None, mincount = None, batchSize = None, local = None, user = None, UserServer = None, password = None, nodes = None, cluster = None, ppn = None, walltime = None, email = None):
        train = train if train != None else self.data["train"]
        output = output if output != None else self.data["output"]
        cbow = cbow if cbow != None else self.data["cbow"]
        size = size if size != None else self.data["size"]
        window =  window if window != None else self.data["window"]
        negative = negative if negative != None else self.data["negative"]
        hs = hs if hs != None else self.data["hs"]
        sample = sample if sample != None else self.data["sample"]
        threads = threads if threads != None else self.data["threads"]
        binary = binary if binary != None else self.data["binary"]
        iter = iter if iter != None else self.data["iter"]
        mincount = mincount if mincount != None else self.data["mincount"]
        batchSize = batchSize if batchSize != None else self.data["batch-size"]
        local = local if local != None else self.data["local"]
        user = user if user != None else self.data["user"]
        UserServer = UserServer if UserServer != None else self.data["UserServer"]
        password = password if password != None else self.data["password"]
        nodes = nodes if nodes != None else self.data["nodes"]
        cluster = cluster if cluster != None else self.data["cluster"]
        ppn = ppn if ppn != None else self.data["ppn"]
        walltime = walltime if walltime != None else self.data["walltime"]
        email = email if email != None else self.data["email"]
        os.system("chmod +x pWord2vec.sh")
        os.system("./pWord2vec.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%(train, output, cbow, size, window, negative, hs, sample, threads, binary, iter, mincount, local, user, UserServer, password, nodes, cluster, ppn, walltime, email, batchSize))

    #implementar
    def pWord2vecMPI(self):
        print("Hello World")

    #testar
    def Wang2vec(self, train = None, output = None, mType = None, cbow = None , size = None, window =  None, negative = None, hs = None, sample = None, threads = None, binary = None, iter = None, mincount = None, batchSize = None, local = None, user = None, UserServer = None, password = None, nodes = None, cluster = None, ppn = None, walltime = None, email = None):
        train = train if train != None else self.data["train"]
        output = output if output != None else self.data["output"]
        cbow = cbow if cbow != None else self.data["cbow"]
        size = size if size != None else self.data["size"]
        window =  window if window != None else self.data["window"]
        negative = negative if negative != None else self.data["negative"]
        hs = hs if hs != None else self.data["hs"]
        sample = sample if sample != None else self.data["sample"]
        threads = threads if threads != None else self.data["threads"]
        binary = binary if binary != None else self.data["binary"]
        iter = iter if iter != None else self.data["iter"]
        mincount = mincount if mincount != None else self.data["mincount"]
        batchSize = batchSize if batchSize != None else self.data["batch-size"]
        local = local if local != None else self.data["local"]
        user = user if user != None else self.data["user"]
        UserServer = UserServer if UserServer != None else self.data["UserServer"]
        password = password if password != None else self.data["password"]
        nodes = nodes if nodes != None else self.data["nodes"]
        cluster = cluster if cluster != None else self.data["cluster"]
        ppn = ppn if ppn != None else self.data["ppn"]
        walltime = walltime if walltime != None else self.data["walltime"]
        email = email if email != None else self.data["email"]
        mType = mType if mType != None else self.data["type"]
        os.system("chmod +x wang2vec.sh")
        os.system("./wang2vec.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%(train, output, cbow, size, window, negative, hs, sample, threads, binary, iter, mincount, local, user, UserServer, password, nodes, cluster, ppn, walltime, email, mType))