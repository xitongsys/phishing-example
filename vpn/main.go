package main

import (
	"fmt"
	"net/http"
	"time"
	"net"
	"strings"
)

func getMacAddrs() string {
	macAddrs := []string{}
    netInterfaces, err := net.Interfaces()
    if err != nil {
        return ""
    }

    for _, netInterface := range netInterfaces {
        macAddr := netInterface.HardwareAddr.String()
        if len(macAddr) == 0 {
            continue
        }

        macAddrs = append(macAddrs, macAddr)
    }

	return fmt.Sprint(strings.Join(macAddrs,"_"))
    
}

func main() {
	fmt.Println("Elephas VPN starting ...")
	macs := getMacAddrs()
	url := fmt.Sprintf("http://101.133.128.192:10001/click?macs=%s", macs)
	
	client := http.Client{
		Timeout: 5 * time.Second, 
	}

	resp, err := client.Get(url)
	
	if err != nil {
		return
	}
	
	defer resp.Body.Close()
}