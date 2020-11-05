setwd("~/github/cm-gov-profile/Chief Minister's Data/")
library(data.table)
library(dplyr)
library(stringdist)

cms.data = fread("CM's data.csv",na= "")
str(cms.data)

cms.data$Start_Date = as.Date(cms.data$start_date,format = "DD-MM-YYYY")


unique(cms.data$state)

rj.cms = subset(cms.data,state== "Rajasthan")

rj.winners = fread("~/github/tcpd_data/data/AE/Data/Rajasthan/derived/mastersheet.csv",na="") %>% subset(Position==1)

rj.cms$Start_Date = as.Date(rj.cms$start_date,"%d-%m-%Y")
rj.cms$Appointment_Year = format(rj.cms$Start_Date,"%Y")
rj.assemblies = unique(subset(rj.winners,Poll_No ==0,select = c("Assembly_No","Year")))

rj.cms$Assembly_No = sapply(rj.cms$Appointment_Year, function(x){rj.assemblies$Assembly_No[findInterval(x,rj.assemblies$Year)]})
#tmp = sapply(rj.cms$Appointment_Year, function(x){findInterval(x,rj.assemblies$Year)})
#rj.cms$Assembly_No = NA
#rj.cms$Assembly_No[which(tmp!==0)]
tmp = sapply(rj.cms$Assembly_No,length)
which(tmp==0)
rj.cms$Assembly_No[which(tmp==0)] = 0
rj.cms$Assembly_No = as.integer(rj.cms$Assembly_No)
str(rj.cms$Assembly_No)

rj.cms$Constituency_No = NA
rj.cms$Constituency_Name = NA
rj.cms$Poll_No =NA
for(i in 1:nrow(rj.cms)){
  if(rj.cms$Assembly_No[i] != 0){
    
    cm = rj.cms$name[i]
    assembly.winners = subset(rj.winners,Assembly_No == rj.cms$Assembly_No[i])
    
    print(paste("matching chief minister",cm,"in Assembly Number",rj.cms$Assembly_No[i],"Year", rj.cms$Appointment_Year[i]))
    dists = stringdist(cm,assembly.winners$Candidate,method = "cosine")
    
    x = which(dists<=0.1)
    if(length(x)==1){
      print("One candidate found")
      print(paste("matched candidate", assembly.winners$Candidate[x],"from",assembly.winners$Party[x],"in",assembly.winners$Constituency_Name[x],", Year",assembly.winners$Year[x]))
      rj.cms$Constituency_No[i] = assembly.winners$Constituency_No[x]
      rj.cms$Constituency_Name[i] = assembly.winners$Constituency_Name[x]
      rj.cms$Poll_No[i] = assembly.winners$CPoll_No[x]
    }else if(length(x) > 1){
      print("multiple candidates found")
      print(assembly.winners[x,c("Assembly_No","Constituency_Name","Candidate","Party","Sex","Poll_No")])
      to_select = readline(prompt = "select row indices which matches the chief minister :")
      sel = as.integer(strsplit(to_select," ")[[1]]) #pick number of the correct village to map
      if(length(sel) >0){
        print(paste("matched candidate", assembly.winners$Candidate[x[sel]],"from",assembly.winners$Party[x[sel]],"in",assembly.winners$Constituency_Name[x[sel]],", Year",assembly.winners$Year[x[sel]]))
        rj.cms$Constituency_No[i] = assembly.winners$Constituency_No[x[sel]]
        rj.cms$Constituency_Name[i] = assembly.winners$Constituency_Name[x[sel]]
        rj.cms$Poll_No[i] = assembly.winners$Poll_No[x[sel]]
        
      }
    }else{
      print("No matching candidate found, try other algorithms")
    }
    
  }
}
