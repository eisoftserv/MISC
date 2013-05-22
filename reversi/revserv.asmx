<%@ WebService Language="C#" Class="revserv" %>

using System;
using System.Web;
using System.Web.Services;
using System.Web.Services.Protocols;

[WebService(Namespace = "ellailona.gmail.com")]
[WebServiceBinding(ConformsTo = WsiProfiles.BasicProfile1_1)]
[System.Web.Script.Services.ScriptService]
public class revserv  : System.Web.Services.WebService {

    [WebMethod]
    public string revdispatcher(string ticket, string oper, string data) 
    {
        string result = revcheckinput(ticket, oper, data);
        if (result != "ok") return (result);
        
        int ntrials = 20, npause = 3000;
        string resp="er";
        
        switch (oper)
        {
            case "cc":  // canceling
                resp = "cc";
                Application[ticket] = new revtoken("cc", data);
                break;

            case "tt":  // timeout
                resp = "tt";
                Application[ticket] = new revtoken("tt", data);
                break;
                
            case "ee":  // end game
                resp = "ee";
                Application[ticket] = new revtoken("ee", data);
                break;
                
            case "sb":  // server begin - sending game scheme
                resp=serverconnect(data, ticket, ntrials, npause);
                break;

            case "cb":  // client begins - getting game scheme
                resp=doloop("cb", "sb", "cb", data, ticket, ntrials, npause);
                break;

            case "cr":  // client read - getting first server movement
                resp=doloop("cr", "sd", "cg", data, ticket, ntrials, npause);                
                break;

            case "cd":  // client data - movement
                resp=doloop("cd", "sd", "cg", data, ticket, ntrials, npause);                                
                break;

            case "sd":  // server data - movement
                resp=doloop("sd", "cd", "sg", data, ticket, ntrials, npause);                
                break;
        } // switch

        return (resp);
        
    } // end revdispatcher

    public struct revtoken
    {
        public string oper;
        public string data;
        public DateTime stamp;

        public revtoken(string inoper, string indata)
        {
            oper = inoper;
            data = indata;
            stamp = DateTime.UtcNow;
        }

        public int getdif()
        {
            DateTime current = DateTime.UtcNow;
            double dif = current.Ticks / 10000000 - this.stamp.Ticks / 10000000;
            return (int)dif;
        }
    }

    protected string doloop(string who, string what, string where, string data, string ticket, int ntrials, int npause)
    {
        string resp = "tt";
        revtoken rt;

        if (who == "cd" || who == "sd")
        {
            if (Application[ticket] != null)
            { rt = (revtoken)Application[ticket]; }
            else
            { return ("erticket not found"); }
            
            if (rt.oper=="cc") return ("cc");
            Application[ticket] = new revtoken(who, data);
        }
        
        for (int i = 0; i < ntrials; i++)
        {
            if (Application[ticket] != null)
            { rt = (revtoken)Application[ticket]; }
            else
            {
                resp = "erticket not found";
                break;  
            }
            if (who!="cb")
            {
                if (rt.oper == "cc")  // canceling
                {
                    resp = "cc";
                    break;
                }
                if (rt.oper == "tt")  // timeout
                {
                    resp = "tt";
                    break;
                }
                if (rt.oper == "ee")  // end game
                {
                    resp = "ee";
                    break;
                }       
            }     
            if (rt.oper == what)
            {
                resp = "ok" + rt.data;
                Application[ticket] = new revtoken(where, data);
                break;
            }
            System.Threading.Thread.Sleep(npause);
        }
        return resp;
    }

    protected string serverconnect(string data, string ticket, int ntrials, int npause)
    {
        string resp = "tt";
    // checking the timestamp
        revtoken rt = (revtoken)Application[ticket];
        if (rt.getdif() > 1800)
        {
            Application.Remove(ticket);
            return ("erticket removed due to expiration");
        }
  // because at client-side the same message could be re-sent more times...
        if (rt.oper != "cb") Application[ticket] = new revtoken("sb", data);
        for (int i = 0; i < ntrials; i++)
        {
            if (Application[ticket] != null)
            { rt = (revtoken)Application[ticket]; }
            else
            {
                resp = "erticket not found";
                break;
            }
            if (rt.oper == "cc")
            {
                resp = "cc";
                break;
            }
            if (rt.oper == "cb")
            {
                resp = "ok";
                break;
            }
            System.Threading.Thread.Sleep(npause);
        }
        
        return resp;
    }
    
    protected string revcheckinput(string ticket, string oper, string data)
    {
        if (ticket=="demo") return ("erservice not available in DEMO");
        string[] opers = new string[] { "sb", "cb", "cr", "sd", "cd", "cc", "ee", "tt" };
        int pos = Array.IndexOf(opers, oper);
        if (pos < 0) return ("erunknown operation: " + oper);

        if (Application[ticket] == null)
        {
            if (oper=="sb" || oper=="cb")
            {
                if (oper == "sb" && data != "1" && data != "2") return ("erunknown scheme: " + data);
                Application[ticket] = new revtoken("nd", "");
                return ("ok");
            }
            else
            {
                return ("erno ticket found for operation: " + oper);
            }
        }
        
        revtoken token = (revtoken)Application[ticket];
        if (token.getdif()>900) // 
        {
            Application.Remove(ticket);
            return ("erticket removed due to 15 minute time limit between operations");
        }

        return "ok";       
    } // revcheckinput
    
} // service