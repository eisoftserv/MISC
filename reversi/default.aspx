<%@ Page Language="C#" AutoEventWireup="true" CodeFile="default.aspx.cs" Inherits="revpage" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Reversi</title>
    <script type="text/javascript" src="./revpic.js"></script>
</head>
<body onload="myonload()" style="width: 600px; margin:0 auto;">

    <form id="form1" runat="server" 
    style="font-family: Verdana; font-size: medium; color: #3399FF; font-weight: bold;">

    <asp:ScriptManager ID="ScriptManager1" runat="server">
        <Services>
        <asp:ServiceReference Path="./revserv.asmx" />
        </Services>
    </asp:ScriptManager>

    <script type="text/javascript" src="./revclient.js"></script>

    <br />
    <asp:Panel ID="PanelHead" runat="server" Height="48px" Width="600px">

        <asp:Panel ID="PanelStart" runat="server" Height="48px" Width="48px" style="position: relative;left:16px;">
            <asp:ImageButton ID="imagestart" runat="server" Width="48px" Height="48px" style="margin:-8px 0 0 0;"
                ImageUrl="" OnClientClick="return startbuttonclick()" 
                EnableViewState="False" ViewStateMode="Disabled" ToolTip="START..." />
        </asp:Panel>

        <asp:Panel ID="PanelText" runat="server" style="left: 78px; position: relative; height: 48px; width: 250px; top: -48px;text-align:center;">
            <asp:Label ID="headtext" runat="server" Text="Reversi" 
            Width="308px" Height="48px" Font-Bold="True" 
            Font-Names="Verdana" Font-Size="X-Large"></asp:Label>
         </asp:Panel>

        <asp:Panel ID="PanelHoldScore" runat="server" 
            style="left: 312px; position: relative; height: 36px; width: 128px; top: -96px;text-align:center;">
        <asp:Panel ID="PanelScore" runat="server"
            style="width:128px;height:36px;border-radius:8px;box-shadow:4px 4px 2px 2px #AABBCC;" >
            <asp:Label ID="scoreboard" runat="server" Text="88:88" 
            Font-Bold="True" Font-Names="Verdana" Font-Size="X-Large"></asp:Label>
        </asp:Panel>
        </asp:Panel>

        <asp:Panel ID="PanelCancel" runat="server" Height="48px" Width="48px"  style="left: 534px; position: relative; top: -134px;">
                    <asp:ImageButton ID="imagecancel" runat="server" Width="48px" Height="48px"
                    ImageUrl="" OnClientClick="return mycancelclick()" 
                    EnableViewState="False" ViewStateMode="Disabled" ToolTip="Help" />
        </asp:Panel>

    </asp:Panel>
    
    <asp:Panel ID="PanelOptions" runat="server" Height="600px" Width="600px">
        <br />
        <asp:CheckBox ID="CheckServer" runat="server" Text="Soy invitador(a)" 
            onclick="changeserverstatus()" ToolTip="I am the inviter" />
        <br />
        <br />
        <asp:Panel ID="PanelScheme" runat="server" Height="60px" Width="360px">
            <asp:Label ID="Label1" runat="server" Text="Tipo de apertura preferida:"
                EnableViewState="False" ViewStateMode="Disabled" 
                ToolTip="The preferred opening scheme"></asp:Label>
            <br />
            <br />
            <asp:Image ID="imagea" runat="server" style="height:40px;width:40px;border-radius:8px;box-shadow:0 0 4px #778899;"
                ImageUrl="" EnableViewState="False" 
                ViewStateMode="Disabled" />
            <asp:RadioButton ID="RadioAp1" runat="server" 
                style="top: -15px; position: relative; left: 5px;" GroupName="apertura" />
            <asp:Image ID="imageb" runat="server" style="height:40px;width:40px;left: 10px; position: relative;border-radius:8px;box-shadow:0 0 4px #778899;"
                ImageUrl=""
                EnableViewState="False" ViewStateMode="Disabled" />
            <asp:RadioButton ID="RadioAp2" runat="server" 
                style="top: -15px; position: relative; left: 15px" GroupName="apertura" />
        </asp:Panel>
        <br />
        <br />
    <asp:Panel ID="PanelBoard" runat="server" Height="70px" Width="500px">
        <asp:Label ID="Label2" runat="server" Text="El color del tablero:"
            EnableViewState="False" ViewStateMode="Disabled" ToolTip="Table color"></asp:Label>
        <br />
            <br />
        <asp:RadioButton ID="RadioBo1" runat="server" Width="60px" BorderColor="White" style=" border-radius:8px;box-shadow:0 0 4px #778899;"
            BorderStyle="Solid" Height="50px" GroupName="tablero" />
        <asp:RadioButton ID="RadioBo2" runat="server" Width="60px" BorderColor="White" style=" border-radius:8px;box-shadow:0 0 4px #778899;"
            BorderStyle="Solid" Height="50px" GroupName="tablero" />
        <asp:RadioButton ID="RadioBo3" runat="server" Width="60px" BorderColor="White" style=" border-radius:8px;box-shadow:0 0 4px #778899;"
            BorderStyle="Solid" Height="50px" GroupName="tablero" />
        <asp:RadioButton ID="RadioBo4" runat="server" Width="60px" BorderColor="White" style=" border-radius:8px;box-shadow:0 0 4px #778899;"
            BorderStyle="Solid" Height="50px" GroupName="tablero" />
    </asp:Panel>
        <br />
        <br />

    <asp:Panel ID="PanelElem" runat="server" Height="70px" Width="500px">
        <asp:Label ID="Label3" runat="server" Text="El color de las fichas oscuras:"
            ToolTip="The color of the dark chips"></asp:Label>
        <br />
            <br />
        <asp:RadioButton ID="RadioFi1" runat="server" Width="60px" BorderColor="White" style=" border-radius:8px;box-shadow:0 0 4px #778899;"
            BorderStyle="Solid" Height="50px" GroupName="ficha" />
        <asp:RadioButton ID="RadioFi2" runat="server" Width="60px" BorderColor="White" style=" border-radius:8px;box-shadow:0 0 4px #778899;" 
            BorderStyle="Solid" Height="50px" GroupName="ficha" />
        <asp:RadioButton ID="RadioFi3" runat="server" Width="60px" BorderColor="White" style=" border-radius:8px;box-shadow:0 0 4px #778899;" 
            BorderStyle="Solid" Height="50px" GroupName="ficha" />
        <asp:RadioButton ID="RadioFi4" runat="server" Width="60px" BorderColor="White" style=" border-radius:8px;box-shadow:0 0 4px #778899;" 
            BorderStyle="Solid" Height="50px" GroupName="ficha" />

    </asp:Panel>

    </asp:Panel>

    <asp:Panel ID="PanelDown" runat="server" style="width:600px;height:600px;border-radius:8px;box-shadow:4px 4px 4px 4px #AABBCC;"
        ViewStateMode="Enabled">

    <asp:DataList ID="boa" runat="server" style="width:600px;height:600px;"
        RepeatColumns="8" 
        RepeatDirection="Horizontal" ShowFooter="False" ShowHeader="False">

    <ItemTemplate>
        <input id="ibu" runat="server" type="button" value="" style="width:72px;height:72px;border-collapse:collapse;border-radius:8px;border:thin solid #FFFFFF;"
        onclick="<%# Container.DataItem %>"  />

     </ItemTemplate>

    </asp:DataList>

    </asp:Panel>


    <div style="width:600px;text-align:center;">

        <asp:ImageButton ID="company" runat="server" ImageUrl=""
        OnClientClick="return goback()"
         style="width:72px;height:36px;margin:16px auto;" />

   </div>

    <div id="modala" style="width:400px;margin:0 100px;border-radius:16px;box-shadow:0 0 16px #778899;background-color:#FFFFEE;font-family:Verdana;font-size:medium;font-weight:bolder;">
        <div style="text-align:right;margin:10px 0 -10px 0;">
        <a href="" onclick="return bilialert.hide()" style="font-size:large;text-decoration:none;color:#44AAFF;margin:0 20px 0 0;" >X</a>
        </div>
        <div id="modales" style="width:360px;margin:auto 20px;color:#FF9933"></div>
        <div id="modalen" style="width:360px;margin:auto 20px;color:#44AAFF"></div>
        <br />
    </div>


  <asp:HiddenField ID="mydata" runat="server" />
    
    
    </form>
</body>
</html>
