<%@ Page Language="C#" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<script runat="server">

    protected void Page_Load(object sender, EventArgs e)
    {
        if (Request.QueryString["es"] != null)
            Label1.Text = HttpUtility.UrlDecode((string)Request.QueryString["es"]);
        else Label1.Text = "página en construcción";

        if (Request.QueryString["en"] != null)
            Label2.Text = HttpUtility.UrlDecode((string)Request.QueryString["en"]);
        else Label2.Text = "page under construction";
    }
</script>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server" 
    style="font-family: Verdana; font-size: x-large; text-align: center; color: #990033">
    <asp:Label ID="Label1" runat="server" Font-Bold="True" Font-Names="Verdana" 
        Font-Size="Medium" ForeColor="#FF9933"></asp:Label>
    <br />
    <br />
    <asp:Label ID="Label2" runat="server" Font-Bold="True" Font-Names="Verdana" 
        Font-Size="Medium" ForeColor="#0099FF"></asp:Label>
    <br />
    </form>
</body>
</html>
