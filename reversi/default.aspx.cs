using System;
using System.Collections;
using System.Collections.Generic;
using System.Configuration;
using System.Drawing;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class revpage : System.Web.UI.Page
{
    protected void Page_PreInit(object sender, EventArgs e)
    {
        Session["ticket"] = "test";
    }

    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            PanelDown.Visible = false;

            RadioBo1.BackColor = ColorTranslator.FromHtml("#FF8C78");
            RadioBo2.BackColor = ColorTranslator.FromHtml("#FFB450");
            RadioBo3.BackColor = ColorTranslator.FromHtml("#50C8A0");
            RadioBo4.BackColor = ColorTranslator.FromHtml("#3CC8FF");

            RadioFi1.BackColor = ColorTranslator.FromHtml("#B41414");
            RadioFi2.BackColor = ColorTranslator.FromHtml("#B45A00");
            RadioFi3.BackColor = ColorTranslator.FromHtml("#28785A");
            RadioFi4.BackColor = ColorTranslator.FromHtml("#2882AA");

            RadioAp1.Checked = true;
            RadioBo4.Checked = true;
            RadioFi1.Checked = true;

            mydata.Value = "*";

            ArrayList ar = new ArrayList();
            for (int i = 0; i < 8; i++)
            {
                for (int j = 0; j < 8; j++)
                {
                    ar.Add("return boardbuttonclick(" + (i + 1).ToString() + "," + (j + 1).ToString() + ")");
                }
            }
            boa.DataSource = ar;
            boa.DataBind();

            return;
        } // end first page load
// postback
        if (Session["ticket"]==null )
        {
            string tes = HttpUtility.UrlEncode("falta de tiquet");
            string ten = HttpUtility.UrlEncode("missing ticket");
            Server.Transfer("./revbreak.aspx?es=" + tes + "&en=" + ten); 
        }

        PanelOptions.Visible = false;
        PanelDown.Visible = true;

        string a="A", b="D", c="A", d="B";
        if (RadioAp1.Checked) { a = "A"; }
        if (RadioAp2.Checked) { a = "B"; }

        if (RadioBo1.Checked) { b = "A"; }
        if (RadioBo2.Checked) { b = "B"; }
        if (RadioBo3.Checked) { b = "C"; }
        if (RadioBo4.Checked) { b = "D"; }

        if (RadioFi1.Checked) { c = "A"; }
        if (RadioFi2.Checked) { c = "B"; }
        if (RadioFi3.Checked) { c = "C"; }
        if (RadioFi4.Checked) { c = "D"; }

        d=(CheckServer.Checked ? "A" : "B" );
        mydata.Value = a + b + c + d+Session["ticket"];
     
    } // Page_Load

} // revpage