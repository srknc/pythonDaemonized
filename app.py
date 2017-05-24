import os,sys,signal
from time import sleep

class app(object):
	def __init__(self):
		self.pidfile = '/tmp/app.pid'
	def start(self):
		if os.path.isfile(self.pidfile):
			file = open(self.pidfile, 'r') 
			print "already running ["+file.read()+"]"
			file.close()
		else:
			print "forking"
			try:
				f = os.fork()
				if f > 0:
					# Exit parent process
					sys.exit(0)
			except OSError, e:
				print >> sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
				sys.exit(1)

			# Configure the child processes environment
			os.chdir("/")
			os.setsid()
			os.umask(0)
			spid = os.getpid()

                        try:
                                file = open(self.pidfile, 'w')
                                file.write(str(spid))
				file.close()
                                print "starting ["+str(spid)+"]"
                        except:
                                print "unable to create pid"
                                sys.exit(1)

    			while True:
				self.main()
	        		sleep(10)

	def stop(self):
                try:
                        file = open(self.pidfile, 'r')
			pid = file.read()
			file.close
		except:
			print "failed to get pid"
			sys.exit(1)
		print " -> stopping application ["+pid+"]"
		os.kill(int(pid), signal.SIGTERM)	
		os.remove(self.pidfile)
		

	def main(self):
		print "a"



try:
        if not ( sys.argv[1] == 'start' or sys.argv[1] == 'stop' ):
                raise Exception
        mode=str(sys.argv[1])
except:
        print "usage: python "+sys.argv[0]+" [start/stop]"
        sys.exit(1)

app = app()

if mode == 'start':
	app.start()

if mode == 'stop':
	app.stop()
