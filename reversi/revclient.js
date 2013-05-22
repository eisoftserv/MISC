var lyourpass = false, lmypass = false;
var lserver = false, lwaiting = false, lmodal=false;
var lgameloaded = false, lplaying = false;
var crevfree = "F", crevmy = "M", crevyour = "Y";

var crevstartscheme = "1";
var crevmycolor = "1"; // dark server bright client
var nmycolor = 0, nyourcolor = 0;
var nrevside = 8, nrevdirs = 8, nrevtotbut = 64;
var ncounttimeout = 0;

var nrevtablecolor, nrevdarkcolor, nrevbrightcolor;
var nrevtablecolori = 4, nrevdarkcolori = 1;

var askintable = new Array(5);
var askindark = new Array(5);

var arevtable = new Array(9);
var arevsel = new Array(9);
var arevana = new Array(9);

var arevcaptured = new Array(9);
var arevscore = new Array(3);
var arevmoved = new Array(3);

var objboard = new Array(9);
var objscore, objdyna, objexit;

var transticket, transoper, transdata;

var bilialert = null;

revserv.set_defaultSucceededCallback(transmissionok);
revserv.set_defaultFailedCallback(transmissionerror);

function yamonbeforeunload(e) {
    if (lgameloaded == true && lplaying == true) return "Do you really want to quit?";
}
window.onbeforeunload = yamonbeforeunload;

function goback() {
    if (lgameloaded) return false;
    window.location.replace("../default.aspx");
    return false;
}

function modalalert_show(tes, ten) {
    this.es.innerHTML = "<p>" + tes + "</p>";
    this.en.innerHTML = "<p>" + ten + "</p>";
    this.obj.style.display = "";
    return false;
}

function modalalert_hide() {
    this.obj.style.display = "none";
    return false;
}

function modalalert(name, es, en, zindex) {
    this.obj = document.getElementById(name);
    this.es = document.getElementById(es);
    this.en = document.getElementById(en);
    this.show = modalalert_show;
    this.hide = modalalert_hide;
    this.obj.style.position = "fixed";
    this.obj.style.top = "92px";
    this.obj.style.zIndex = zindex;
    this.obj.style.opacity = "1.0";
}

function settalking(ltalking) {
    lwaiting = ltalking;
    objdyna.style.display = (lwaiting ? "" : "none");
    //objexit.style.display = (lwaiting ? "none" : "");
}

function transmissionok(buff) {
    var inoper = buff.substring(0, 2);
    var indata = buff.substring(2);

    if (inoper == "er") {
        paintcancel("Error de servicio irrecuperable", "Unrecoverable service error: "+indata);
        return null;
    } // logical error

    if (inoper == "cc") {
        paintcancel("El juego ha terminado por solicitúd de cancelación!", "The game has ended due to cancel request!" + indata);
        return null;
    } // partner cancel

    if (inoper == "ee") {
        lplaying = false;
        settalking(false);
        bilialert.show("El juego ha terminado!", "The game is over!");
        lgameloaded = false;
        return null;
    } // game ended on partner side

    if (inoper == "tt") {
        if (ncounttimeout < 2) {
            ncounttimeout++;
            revserv.revdispatcher(transticket, transoper, transdata);
            return null;
        }
        lplaying = false;
        settalking(false);
        paintcancel("El juego ha terminado por tiempo de espera expirado!", "The game has ended due to wait timeout!" + indata);
        return null;
    } else {
        ncounttimeout = 0;
    } // timeout
        

    if (transoper == "sb") {
        revinitparty();
        settalking(false);
        return null;
    } // sb

    if (transoper == "cb") {
        var tmp = indata.substring(0, 1);
        if (tmp != "1" && tmp != "2") {
            paintcancel("Error irrecuperable: se ha recibido tipo de apertura incorrecto: "+tmp, "Fatal error: received wrong starting scheme: " + tmp);
            return null;
        }
        crevstartscheme = tmp;
        revinitparty();

        transoper="cr";
        transdata = "";
        revserv.revdispatcher(transticket, transoper, transdata);
        return null
    } // cb

    if (transoper == "cr" || transoper == "cd" || transoper == "sd") {
        revextractmovement(buff.substring(2));
        lyourpass = (arevmoved[1] > 0 && arevmoved[2] > 0 ? false : true);
        if (!lyourpass) revregister(false);
        revgetselectables();
        lmypass = (!revexistsmove() ? true : false);

        if (lyourpass && lmypass) {
            transoper = "ee"; // end game on my side
            transdata = "";
            revserv.revdispatcher(transticket, transoper, transdata);
            return null;
        }

        if (lmypass) {
            arevmoved[1] = 0;
            arevmoved[2] = 0;
            for (i = 1; i <= nrevdirs; i++) {
                arevcaptured[i] = 0;
            }
            transoper = (lserver ? "sd" : "cd" );
            transdata = revcomposemovement();
            revserv.revdispatcher(transticket, transoper, transdata);
            return null;
        }

        settalking(false);

    } // cr, cd, sd
} // transmissionok


function transmissionerror(err) {
    settalking(false);
    lplaying = false;
    paintcancel("Error de entorno irrecuperable", "Unrecoverable environment error: " + err.get_message());
}


function myonload() {

    document.getElementById("company").src = contentx3;
    bilialert = new modalalert("modala", "modales", "modalen", "99");
    bilialert.hide();
    var obj = document.getElementById("mydata");
    var info=obj.value;
    var val = info.substring(0, 1);
    if ( (info==null) || (val!="*" && val!="A" && val!="B") ) {
        paintcancel("Error de comunicación: mensaje desconocido", "communication error - "+info+" - empty or unknown message");
        return null;
    }

//first pageload
    if (val == "*") {
        lgameloaded = false;
        document.getElementById("RadioAp1").disabled = true;
        document.getElementById("RadioAp2").disabled = true;
        document.getElementById("PanelScore").style.display = "none";
        obj = document.getElementById("imagecancel");
        obj.src = contentx4;
        obj.title = "Ayuda - Help";
        document.getElementById("imagea").src = contentx0;
        document.getElementById("imageb").src = contentx1;
        obj=document.getElementById("imagestart");
        obj.src = contentx2;
        obj.title = "START juego - game";
        return null;
    }
    //postback pageload
    lgameloaded = true;
    crevstartscheme = (val == "A" ? "1" : "2");

    val = info.substring(1, 2);
    if (val<"A" || val>"D") {
        paintcancel("Error de comunicación: mensaje desconocido", "communication error - " + val + " - unknown message");
        return null;
    }
    nrevtablecolori = val.charCodeAt(0) - 64;

    val = info.substring(2, 3);
    if (val < "A" || val > "D") {
        paintcancel("Error de comunicación: mensaje desconocido", "communication error - " + val + " - unknown message");
        return null;
    }
    nrevdarkcolori = val.charCodeAt(0) - 64;

    val = info.substring(3, 4);
    if (val < "A" || val > "B") {
        paintcancel("Error de comunicación: mensaje vacio u desconocido", "communication error - " + val + " - unknown message");
        return null;
    }
    if (val == "A") lserver = true;

    initenvironment();
// proper game start
    transticket = info.substring(4);
    transoper = (lserver ? "sb" : "cb");
    transdata = (lserver ? crevstartscheme : "");
    lplaying = true;
    settalking(true);
    revserv.revdispatcher(transticket, transoper, transdata);
} // myonload


function initenvironment() {
    var obj;

    for (var i = 1; i <= 8; i++) {
        objboard[i] = new Array(9);
        arevtable[i] = new Array(9);
        arevsel[i] = new Array(9);
        arevana[i] = new Array(9);
        for (var j = 1; j <= 8; j++) {
            arevana[i][j] = new Array(9);
        }
    }
    askintable[1] = "#FF8C78";
    askintable[2] = "#FFB450";
    askintable[3] = "#50C8A0";
    askintable[4] = "#3CC8FF";

    askindark[1] = "#B41414";
    askindark[2] = "#B45A00";
    askindark[3] = "#28785A";
    askindark[4] = "#2882AA";

    nrevtablecolor = askintable[nrevtablecolori];
    nrevdarkcolor = askindark[nrevdarkcolori];
    nrevbrightcolor = "#FFFFFF";
    nmycolor=(lserver ? nrevdarkcolor : nrevbrightcolor);
    nyourcolor = (lserver ? nrevbrightcolor : nrevdarkcolor);

    obj = document.getElementById("PanelScore");
    obj.style.backgroundColor = nrevtablecolor;
    obj.style.color = nmycolor;
    obj.style.borderColor = nrevdarkcolor;
    obj.style.display = "";

    objdyna = document.getElementById("imagestart");
    objdyna.style.display = "none";
    objdyna.src = contentz0;
    objdyna.title = "Esperando datos - Waiting for data";

    objexit = document.getElementById("imagecancel");
//    objexit.style.display = "none";
    objexit.src = contentx5;
    objexit.title = "Cancelar - Cancel";

    objscore = document.getElementById("scoreboard");
    objscore.style.display = "none";
    objscore.innerText = " 2 : 2 ";
    objscore.textContent = " 2 : 2 ";

    obj = document.getElementById("headtext");
    obj.style.color = nrevdarkcolor;
    obj.style.display = "";

    var tmp, key;
    var npos,cpos;
    for (var i = 0; i < 8; i++) {
        for (j = 0; j < 8; j++) {
            npos = 8 * i + j;
            if (npos == 0) {
                cpos = "00";
            } else {
                if (npos < 10) {
                    cpos = "0" + String(npos);
                } else {
                    cpos = String(npos);
                }
            }
            //asp.net 3.5
            key = "boa_ctl" + cpos + "_ibu";
            // asp.net 4.0
            //key = "boa_ibu_" + String(8*i+j);
            tmp = document.getElementById(key);
            tmp.style.backgroundColor = nrevtablecolor;
            tmp.style.borderColor = nrevtablecolor;
            objboard[i + 1][j + 1] = tmp;
        }
    }
    tmp = document.getElementById("boa");
    tmp.style.borderColor = nrevtablecolor;
} // end initenvironment


function paintcancel(estext, entext) {
    lplaying = false;
    settalking(false);
    var obj = document.getElementById("PanelHead");
    if (obj != null) obj.style.display = "none";
    var obj = document.getElementById("PanelOptions");
    if(obj!=null) obj.style.display = "none";
    var obj = document.getElementById("PanelDown");
    if (obj != null) obj.style.display = "none";
    lgameloaded = false;
    bilialert.show(estext, entext);
}

function startbuttonclick() {
    if (lmodal) return false;
    if (!lgameloaded) {
        lmodal = true;
        document.getElementById("PanelOptions").style.display = "none";
        document.getElementById("imagestart").style.display = "none";
        document.getElementById("headtext").style.display = "none";
        lmodal = false;
        return true;
    }
    return false;
}


function boardbuttonclick(nlin, ncol) {
    if (lmodal) return false;
    if (lwaiting || !lplaying) return false;
   var i=0;
   var cstringtosend=""

   if (!arevsel[nlin][ncol]) {
       bilialert.show("Selección incorrecta!", "Inappropiate selection!");
       return false;
   }
   lmodal = true;
   arevmoved[1]=nlin;
   arevmoved[2]=ncol;
   for (i=1; i<=nrevdirs; i++) {
      arevcaptured[i]=arevana[nlin][ncol][i];
   }

  revregister(true);

  transoper = (lserver ? "sd" : "cd");
  transdata = revcomposemovement();
  settalking(true);
  lmodal = false;
  revserv.revdispatcher(transticket, transoper, transdata);

  return false;
}  // boardbuttonclick


function revregister(lmy) {
   var i, j, k, l;
   var nlin=0, ncol=0, nitems=0;
   var cscore="";
   var rr;
   nlin=arevmoved[1];
   ncol=arevmoved[2];
   arevtable[nlin][ncol]=(lmy ? crevmy : crevyour);
   revdisplaycell(nlin, ncol, lmy);
   
   for (i=1; i<=nrevdirs; i++) {
      nitems=arevcaptured[i];
      j=nlin;
      k=ncol;
      for (l=1; l<=nitems; l++) {
         rr=revdirworkup(i, j, k);
         j=rr[0];
         k=rr[1];
         arevtable[j][k]=(lmy ? crevmy : crevyour);
         revdisplaycell(j, k, lmy);
      }
   }
   
   arevscore[1]=0;
   arevscore[2]=0;
   for (i=1; i<=nrevside; i++) {
      for (j=1; j<=nrevside; j++) {
         if (arevtable[i][j] == crevmy) {
            arevscore[1]=arevscore[1]+1;
         } else {
            if (arevtable[i][j] == crevyour) arevscore[2]=arevscore[2]+1;
         }
      }
   }

    cscore = String(" "+arevscore[1]) + " : " + String(arevscore[2]+" ");
    objscore.innerText=cscore;
    objscore.textContent=cscore;
}


function revexistsmove() {
   var i=0, j=0;
   var lexists=false;
   for (i=1; i<=nrevside; i++) {
      for (j=1; j<=nrevside; j++) {
         if (arevsel[i][j]) {
            lexists=true;
            break;
         }
      }
      if (lexists) break;
   }
   return (lexists);
}


function revdisplaycell(nlin, ncol, lmy) {
    objboard[nlin][ncol].style.backgroundColor = (lmy == true ? nmycolor : nyourcolor);
}


function revcomposemovement() {
   var i;
   var ctocompose="";
   for (i=1; i<=2; i++) {
      ctocompose=ctocompose+String(arevmoved[i]);
   }
   for (i=1; i<=nrevdirs; i++) {
      ctocompose=ctocompose+String(arevcaptured[i]);
   }
return (ctocompose+" ");
}


function revextractmovement(ctoextract) {
   var i;
   for (i=1; i<=2; i++) {
      arevmoved[i]=parseInt(ctoextract.substring(i-1, i));
   }
   for (i=1; i<=nrevdirs; i++) {
      arevcaptured[i]=parseInt(ctoextract.substring( i+1, i+2));
   }
   return null;
}


function revdirworkup(i, j, k) {
   switch (i) {
   case 1:  // north
      j=j-1;
      break;
   case 2:  // north-east
      j=j-1;
      k=k+1;
      break;
   case 3:  // east
      k=k+1;
      break;
   case 4:  // south-east
      j=j+1;
      k=k+1;
      break;
   case 5:  // south
      j=j+1;
      break;
   case 6:  // south-west
      j=j+1;
      k=k-1;
      break;
   case 7:  // west
      k=k-1;
      break;
   case 8:  // north-west
      j=j-1;
      k=k-1;
      break;
   } // switch
   
   var rr=new Array(2);
   rr[0]=j;
   rr[1]=k;
return (rr);
} // revdirworkup


function revgetselectables() {
   var i, j, k;
   for (i=1; i<=nrevside; i++) {
      for (j=1; j<=nrevside; j++) {
         arevsel[i][j]=false;
         for (k=1; k<=nrevdirs; k++) {
            arevana[i][j][k]=0;
         }
      }
   }
   for (i=1; i<=nrevside; i++) {
      for (j=1; j<=nrevside; j++) {
         if (arevtable[i][j] == crevfree) revgetselectable(i,j);
      }
   }
} // revgetselectables


function revgetselectable(nline, ncol) {
   var i=0, j=0, k=0, nsel=0;
   var lmine=false;
   var rr;
   for (i=1; i<=nrevdirs; i++) {
      nsel=0;
      j=nline;
      k=ncol;
      lmine=false;
      while (true) {
         rr=revdirworkup(i, j, k);
         j=rr[0];
         k=rr[1];
         if (j<1 || k<1 || j>nrevside || k>nrevside) break;
         if (arevtable[j][k] == crevfree) break;
         if (arevtable[j][k] == crevyour) {
            nsel=nsel+1;
         } else {
            lmine=true;
            break;
         }
      } // while
      if (nsel>0 && lmine==true ) arevana[nline][ncol][i]=nsel;
   }     // directions

   for (i=1; i<=nrevdirs; i++) {
      if (arevana[nline][ncol][i] > 0) {
         arevsel[nline][ncol]=true;
         break;
      }
   }
   return null;
} // revgetselectable


function revinitparty() {
    var i, j, k;
   var cdark = (lserver ? crevmy : crevyour);
   var cbright = (!lserver ? crevmy : crevyour);
   
   for (i=1; i<=2; i++) {
      arevscore[i]=2;
      arevmoved[i]=0;
   }
   
   for (i=1; i<=nrevside; i++) {
      for (j=1; j<=nrevside; j++) {
         arevsel[i][j]=false;
         arevtable[i][j]=crevfree;
         for (k=1; k<=nrevdirs; k++) {
            arevana[i][j][k]=0;
         }
      }
   }
   
   for (i=1; i<=nrevdirs; i++) {
      arevcaptured[i]=0;
   }

   scoreboard.style.display = "";
   
   arevtable[4][4]=(crevstartscheme=="1" ? cdark : cdark);
   arevtable[4][5]=(crevstartscheme=="1" ? cbright : cbright);
   arevtable[5][4]=(crevstartscheme=="1" ? cbright : cdark);
   arevtable[5][5]=(crevstartscheme=="1" ? cdark : cbright);
   
   for (i=4; i<=5; i++) {
      for (j=4; j<=5; j++) {
         revdisplaycell(i, j, (arevtable[i][j]==crevmy ? true : false));
      }
   }

   if (lserver) revgetselectables();

} // end revinitparty


function mycancelclick() {
    // exit game
    if (lmodal) return false;
    if (!lgameloaded) {
        bilialert.show("Uno de los jugadores se marca como 'invitador' y elige el tipo de apertura; el otro jugador siempre va a recibir las fichas blancas. Cuando ambos jugadores estan listos para empezar, cliquean en sus botones 'start'. El tiempo de espera es de tres minutos para conectarse o para hacer una movida.",
                         "One of the gamers sets himself as inviter and chooses the starting scheme; the other gamer will always receive the white chips. When both gamers are ready, they click on their 'start' buttons. The timeout for connecting or making a movement is of three minutes.");
        return false;
    }
//    if (lwaiting || !lplaying) return false;
    if (!lplaying) return false;
    lmodal = true;
    transoper = "cc";  // cancel request
    transdata = "";
    settalking(true);
    lmodal = false;
    revserv.revdispatcher(transticket, transoper, transdata);
    return false;
}

function changeserverstatus() {
    var objcheck = document.getElementById("CheckServer");
    var obj1 = document.getElementById("RadioAp1");
    var obj2 = document.getElementById("RadioAp2");
    if (objcheck.checked) { 
        obj1.disabled=false;
        obj2.disabled=false;
    } else {
        obj1.disabled=true;
        obj2.disabled=true;
    }
}