import urllib2
import threading
import requests
import time

total_size = 0
def handler(start,end,url,filename,thread_id):
    # headers = {'Range': 'bytes=%d-%d' % (start, end)}
    # r = requests.get(url,headers = headers, stream = True)
    global total_size
    global file_size
    global start_time
    with  open(filename,"r+b") as fp:
        fp.seek(start)
        buff_sz = 8192
        size = end - start + 1
        temp_start = start
        temp_end = (start+buff_sz)
        if thread_id == 1:
            prev_time = start_time
            prev_total_size = 0
        if temp_end > end:
            temp_end = end
        d_size = 0
        print "thread " + str(thread_id) + " started!"
        while(True):
            headers = {'Range': 'bytes=%d-%d' % (temp_start, temp_end)}
            r = requests.get(url,headers = headers, stream = True)
            fp.seek(temp_start)
            d_size += (temp_end - temp_start + 1)
            total_size += (temp_end - temp_start + 1)
            buff = r.content
            fp.write(buff)
            j = 0
            if thread_id == 1:
                curr_time = time.clock()
                curr_total_size = total_size
                # print "downloaded "+ str(total_size)+" "+str(total_size*100/file_size)+"% "+str(int(((curr_total_size - prev_total_size)/(curr_time-prev_time))/1000))+"kB/s"
                prev_total_size = curr_total_size
                prev_time = curr_time
            # print "Thread "+str(thread_id)+" downloaded "+ str(d_size)+" which makes it "+str(d_size*100/file_size)+"%"
            temp_start = temp_end + 1
            if temp_end == end:
                break
            temp_end = (temp_end + buff_sz)
            if temp_end > end:
                temp_end = end


        # fp.write(r.content)

url_of_file = "http://dl.blugaa.com/lq.blugaa.com/cdn6/4914fd9a9b33a4dc1dcdd915f776b3b6/jqkuv/Joganiyan-(Mr-Jatt.com).mp3"

# @click.command(help="It downloads the specified file with specified name")
# @click.option('--number_of_threads',default=4, help="No of Threads")
# @click.option('--name',type=click.Path(),help="Name of the file with extension")
# @click.argument('url_of_file',type=click.Path())
# @click.pass_context

number_of_threads = 4
start_time = time.clock()
print start_time
print "----"
print "hii"

u = urllib2.urlopen(url_of_file)
meta = u.info()
print meta
file_size = int(meta.getheaders("Content-Length")[0])
print file_size
file_name = url_of_file.split('/')[-1]

print "file size is %d" %file_size

part = int(file_size) / number_of_threads
fp = open(file_name,"wb")
fp.write('\0'*file_size)
fp.close()

print "downloading..about to start"
i = 0

for i in range(number_of_threads):
    start = part*i
    end = start + part
    print str(start) +" to "+ str(end)
    t = threading.Thread(target = handler, kwargs = {'start':start, 'end':end, 'url':url_of_file, 'filename':file_name, 'thread_id':i})
    t.setDaemon(True)
    t.start()
# ----------------------------------------------------------------------------
main_thread = threading.current_thread()
for t in threading.enumerate():
    if t is main_thread:
        continue
    t.join()

print '%s downloaded' % file_name

print "time lapsed: "+str(time.clock() - start_time)

# if __name__ == '__main__':
#     download_file()
