# coding: utf-8
"""
********************************************************************************
* Fichier     : generateAndSendM3U                                             *
* Auteur      : Alexandre FIGARD                                               *
* Mail 	      : contact@alexandre.figard.fr                                    *
* Date        : November 2022                                                  *
* Description : Retrieve and Send the playlist                                 *
********************************************************************************
"""

""" Import of all the necessary libraries """
import requests, xmltodict, smtplib
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


""" Configuration of the server """
path = "/var/www/html/"
server = "YOUR_SERVER_IP"
port = YOUR_SERVER_PORT
protocol = "YOUR_PROTOCOL"

""" Retrieve the media from the UPnP server """


def retrieveMediaFromServer(protocol, server, port):
    """Header of the request"""
    header = {
        "User-Agent": "gupnp-av-cp GUPnP/0.18.1 DLNADOC/1.50",
        "Accept": "",
        "Content-Type": 'text/xml; charset="utf-8"',
        "SOAPAction": '"urn:schemas-upnp-org:service:ContentDirectory:1#Search"',
        "Accept-Language": "en-us;q=1, en;q=0.5",
        "Accept-Encoding": "gzip",
    }
    soap_envelope = '<?xml version="1.0" encoding="UTF-8" ?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><s:Body><u:Search xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"><ContainerID>0</ContainerID><SearchCriteria>(dc:title contains "")</SearchCriteria><Filter>*</Filter><StartingIndex>0</StartingIndex><RequestedCount>100</RequestedCount><SortCriteria>+dc:title</SortCriteria></u:Search></s:Body></s:Envelope>'
    """ Send the request """
    res = requests.post(
        url=str(str(protocol) + "://" + str(server) + ":" + str(port)),
        data=soap_envelope,
        headers=header,
    )
    """ Parse the XML response """
    doc = xmltodict.parse((res.content))
    """ Search for all media in the response """
    items = xmltodict.parse(doc["s:Envelope"]["s:Body"]["u:SearchResponse"]["Result"])[
        "DIDL-Lite"
    ]["item"]

    """ Return the list of media """
    return items


""" Create the playlists with all the media available on the server in different playlists """


def createPlaylist(name, path, mediaList):
    playlist = open(path + name + ".m3u", "w+")
    playlist.truncate(0)
    i = 0
    for media in mediaList:
        if name in media["dc:title"]:
            i += 1
            playlist.write("#EXTINF:" + str(i) + "," + media["dc:title"] + "\n")
            playlist.write(media["res"]["#text"] + "\n")
    playlist.close


""" Create the playlists with all the media available on the server in one playlist """


def createOnePlaylist(item, path):
    playlist = open(path + "playlist" + ".m3u", "w+")
    playlist.truncate(0)
    i = 0
    for media in item:
        playlist.write("#EXTINF:" + str(i) + "," + media["dc:title"] + "\n")
        playlist.write(media["res"]["#text"] + "\n")
    playlist.close


""" Get the list of all name of series and/or movies """


def getSeriesOrMovies(mediaList):
    seriesOrMovies = []
    for media in mediaList:
        serieOrMovie = media["dc:title"][: len(media["dc:title"]) - 7]
        if not (serieOrMovie in seriesOrMovies):
            seriesOrMovies.append(serieOrMovie)

    return seriesOrMovies


""" Create the HTML body of the email """


def createHTMLbody(list):
    body = """\
<!DOCTYPE html>

<html
  lang="en"
  xmlns:o="urn:schemas-microsoft-com:office:office"
  xmlns:v="urn:schemas-microsoft-com:vml"
>
  <head>
    <title></title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <!--[if mso]>
      <xml>
        <o:OfficeDocumentSettings>
          <o:PixelsPerInch>96</o:PixelsPerInch>
          <o:AllowPNG />
        </o:OfficeDocumentSettings>
      </xml>
    <![endif]-->
    <!--[if !mso]><!-->
    <link
      href="https://fonts.googleapis.com/css?family=Roboto"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Abril+Fatface"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Merriweather"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Montserrat"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Nunito"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Bitter"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Permanent+Marker"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Roboto+Slab"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Cabin"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Oxygen"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Oswald"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Lato"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Ubuntu"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Open+Sans"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Droid+Serif"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Playfair+Display"
      rel="stylesheet"
      type="text/css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Poppins"
      rel="stylesheet"
      type="text/css"
    />
    <!--<![endif]-->
    <style>
      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        padding: 0;
      }

      a[x-apple-data-detectors] {
        color: inherit !important;
        text-decoration: inherit !important;
      }

      #MessageViewBody a {
        color: inherit;
        text-decoration: none;
      }

      p {
        line-height: inherit;
      }

      .desktop_hide,
      .desktop_hide table {
        mso-hide: all;
        display: none;
        max-height: 0px;
        overflow: hidden;
      }

      @media (max-width: 700px) {
        .desktop_hide table.icons-inner {
          display: inline-block !important;
        }

        .icons-inner {
          text-align: center;
        }

        .icons-inner td {
          margin: 0 auto;
        }

        .fullMobileWidth,
        .row-content {
          width: 100% !important;
        }

        .mobile_hide {
          display: none;
        }

        .stack .column {
          width: 100%;
          display: block;
        }

        .mobile_hide {
          min-height: 0;
          max-height: 0;
          max-width: 0;
          overflow: hidden;
          font-size: 0px;
        }

        .desktop_hide,
        .desktop_hide table {
          display: table !important;
          max-height: none !important;
        }

        .row-2 .column-1 .block-2.heading_block td.pad {
          padding: 10px 60px 30px !important;
        }

        .row-2 .column-1 .block-2.heading_block h1 {
          font-size: 33px !important;
        }

        .row-4 .column-1 .block-1.heading_block h2 {
          font-size: 20px !important;
        }
      }
    </style>
  </head>
  <body
    style="
      margin: 0;
      background-color: #1a30eb;
      padding: 0;
      -webkit-text-size-adjust: none;
      text-size-adjust: none;
    "
  >
    <table
      border="0"
      cellpadding="0"
      cellspacing="0"
      class="nl-container"
      role="presentation"
      style="
        mso-table-lspace: 0pt;
        mso-table-rspace: 0pt;
        background-color: #1a30eb;
      "
      width="100%"
    >
      <tbody>
        <tr>
          <td>
            <table
              align="center"
              border="0"
              cellpadding="0"
              cellspacing="0"
              class="row row-1"
              role="presentation"
              style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
              width="100%"
            >
              <tbody>
                <tr>
                  <td>
                    <table
                      align="center"
                      border="0"
                      cellpadding="0"
                      cellspacing="0"
                      class="row-content"
                      role="presentation"
                      style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        background-color: #1a30eb;
                        color: #000000;
                        width: 680px;
                      "
                      width="680"
                    >
                      <tbody>
                        <tr>
                          <td
                            class="column column-1"
                            style="
                              mso-table-lspace: 0pt;
                              mso-table-rspace: 0pt;
                              font-weight: 400;
                              text-align: left;
                              vertical-align: top;
                              padding-top: 20px;
                              padding-bottom: 10px;
                              border-top: 0px;
                              border-right: 0px;
                              border-bottom: 0px;
                              border-left: 0px;
                            "
                            width="100%"
                          >
                            <div
                              class="spacer_block"
                              style="
                                height: 45px;
                                line-height: 45px;
                                font-size: 1px;
                              "
                            ></div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table
              align="center"
              border="0"
              cellpadding="0"
              cellspacing="0"
              class="row row-2"
              role="presentation"
              style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                background-size: auto;
              "
              width="100%"
            >
              <tbody>
                <tr>
                  <td>
                    <table
                      align="center"
                      border="0"
                      cellpadding="0"
                      cellspacing="0"
                      class="row-content stack"
                      role="presentation"
                      style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        background-size: auto;
                        background-color: #ffffff;
                        color: #000000;
                        border-bottom: 0 solid #ffffff;
                        border-left: 0 solid #ffffff;
                        border-radius: 30px 30px 0 0;
                        border-right: 0px solid #ffffff;
                        border-top: 0 solid #ffffff;
                        width: 680px;
                      "
                      width="680"
                    >
                      <tbody>
                        <tr>
                          <td
                            class="column column-1"
                            style="
                              mso-table-lspace: 0pt;
                              mso-table-rspace: 0pt;
                              font-weight: 400;
                              text-align: left;
                              vertical-align: top;
                              padding-top: 0px;
                              padding-bottom: 0px;
                              border-top: 0px;
                              border-right: 0px;
                              border-bottom: 0px;
                              border-left: 0px;
                            "
                            width="100%"
                          >
                            <table
                              border="0"
                              cellpadding="0"
                              cellspacing="0"
                              class="heading_block block-2"
                              role="presentation"
                              style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                              "
                              width="100%"
                            >
                              <tr>
                                <td
                                  class="pad"
                                  style="
                                    padding-bottom: 30px;
                                    padding-left: 60px;
                                    padding-right: 60px;
                                    padding-top: 70px;
                                    text-align: center;
                                    width: 100%;
                                  "
                                >
                                  <h1
                                    style="
                                      margin: 0;
                                      color: #020b22;
                                      direction: ltr;
                                      font-family: Poppins, Arial, Helvetica,
                                        sans-serif;
                                      font-size: 40px;
                                      font-weight: 700;
                                      letter-spacing: normal;
                                      line-height: 150%;
                                      text-align: center;
                                      margin-top: 0;
                                      margin-bottom: 0;
                                    "
                                  >
                                    <span class="tinyMce-placeholder">
                                      NEW CONTENT !!
                                    </span>
                                  </h1>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table
              align="center"
              border="0"
              cellpadding="0"
              cellspacing="0"
              class="row row-3"
              role="presentation"
              style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
              width="100%"
            >
              <tbody>
                <tr>
                  <td>
                    <table
                      align="center"
                      border="0"
                      cellpadding="0"
                      cellspacing="0"
                      class="row-content stack"
                      role="presentation"
                      style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        background-color: #ffffff;
                        color: #000000;
                        width: 680px;
                      "
                      width="680"
                    >
                      <tbody>
                        <tr>
                          <td
                            class="column column-1"
                            style="
                              mso-table-lspace: 0pt;
                              mso-table-rspace: 0pt;
                              font-weight: 400;
                              text-align: left;
                              vertical-align: top;
                              padding-top: 0px;
                              padding-bottom: 0px;
                              border-top: 0px;
                              border-right: 0px;
                              border-bottom: 0px;
                              border-left: 0px;
                            "
                            width="100%"
                          >
                            <table
                              border="0"
                              cellpadding="0"
                              cellspacing="0"
                              class="image_block block-1"
                              role="presentation"
                              style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                              "
                              width="100%"
                            >
                              <tr>
                                <td
                                  class="pad"
                                  style="
                                    width: 100%;
                                    padding-right: 0px;
                                    padding-left: 0px;
                                  "
                                >
                                  <div
                                    align="center"
                                    class="alignment"
                                    style="line-height: 10px;"
                                  >
                                    <img
                                      alt="Social profile"
                                      class="fullMobileWidth"
                                      src="images/25d91e8d-79e7-4357-a8f0-24afc98f20e5.png"
                                      style="
                                        display: block;
                                        height: auto;
                                        border: 0;
                                        width: 680px;
                                        max-width: 100%;
                                      "
                                      title="Social profile"
                                      width="680"
                                    />
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table
                              border="0"
                              cellpadding="10"
                              cellspacing="0"
                              class="list_block block-2"
                              role="presentation"
                              style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                word-break: break-word;
                              "
                              width="100%"
                            >
                              <tr>
                                <td class="pad">
                                  <ul
                                    style="
                                      margin: 0;
                                      padding: 0;
                                      margin-left: 20px;
                                      list-style-type: revert;
                                      color: #000000;
                                      font-size: 14px;
                                      font-family: Poppins, Arial, Helvetica,
                                        sans-serif;
                                      font-weight: 400;
                                      line-height: 120%;
                                      text-align: left;
                                      direction: ltr;
                                      letter-spacing: 0px;
                                    "
                                  >                        
                                                        """

    for item in list:
        body += (
            """
                <li>"""
            + item.replace(".", " ")
            + """</li>

                                                                """
        )

    body += """  
                                                                    </ul>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table
              align="center"
              border="0"
              cellpadding="0"
              cellspacing="0"
              class="row row-4"
              role="presentation"
              style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
              width="100%"
            >
              <tbody>
                <tr>
                  <td>
                    <table
                      align="center"
                      border="0"
                      cellpadding="0"
                      cellspacing="0"
                      class="row-content stack"
                      role="presentation"
                      style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        background-color: #f2f5ff;
                        color: #000000;
                        border-radius: 0 0 30px 30px;
                        width: 680px;
                      "
                      width="680"
                    >
                      <tbody>
                        <tr>
                          <td
                            class="column column-1"
                            style="
                              mso-table-lspace: 0pt;
                              mso-table-rspace: 0pt;
                              font-weight: 400;
                              text-align: left;
                              vertical-align: top;
                              padding-top: 15px;
                              padding-bottom: 15px;
                              border-top: 0px;
                              border-right: 0px;
                              border-bottom: 0px;
                              border-left: 0px;
                            "
                            width="100%"
                          >
                            <table
                              border="0"
                              cellpadding="0"
                              cellspacing="0"
                              class="heading_block block-1"
                              role="presentation"
                              style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                              "
                              width="100%"
                            >
                              <tr>
                                <td
                                  class="pad"
                                  style="
                                    padding-bottom: 20px;
                                    padding-top: 20px;
                                    text-align: center;
                                    width: 100%;
                                  "
                                >
                                  <h2
                                    style="
                                      margin: 0;
                                      color: #1a30eb;
                                      direction: ltr;
                                      font-family: Poppins, Arial, Helvetica,
                                        sans-serif;
                                      font-size: 20px;
                                      font-weight: 700;
                                      letter-spacing: normal;
                                      line-height: 120%;
                                      text-align: center;
                                      margin-top: 0;
                                      margin-bottom: 0;
                                    "
                                  >
                                    <span class="tinyMce-placeholder">
                                      Don't be out. Join us.
                                    </span>
                                  </h2>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table
              align="center"
              border="0"
              cellpadding="0"
              cellspacing="0"
              class="row row-5"
              role="presentation"
              style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
              width="100%"
            >
              <tbody>
                <tr>
                  <td>
                    <table
                      align="center"
                      border="0"
                      cellpadding="0"
                      cellspacing="0"
                      class="row-content stack"
                      role="presentation"
                      style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        color: #000000;
                        width: 680px;
                      "
                      width="680"
                    >
                      <tbody>
                        <tr>
                          <td
                            class="column column-1"
                            style="
                              mso-table-lspace: 0pt;
                              mso-table-rspace: 0pt;
                              font-weight: 400;
                              text-align: left;
                              vertical-align: top;
                              padding-top: 5px;
                              padding-bottom: 5px;
                              border-top: 0px;
                              border-right: 0px;
                              border-bottom: 0px;
                              border-left: 0px;
                            "
                            width="100%"
                          >
                            <table
                              border="0"
                              cellpadding="0"
                              cellspacing="0"
                              class="icons_block block-1"
                              role="presentation"
                              style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                              "
                              width="100%"
                            >
                              <tr>
                                <td
                                  class="pad"
                                  style="
                                    vertical-align: middle;
                                    padding-bottom: 5px;
                                    padding-top: 5px;
                                    text-align: center;
                                    color: #9d9d9d;
                                    font-family: inherit;
                                    font-size: 15px;
                                  "
                                >
                                  <table
                                    cellpadding="0"
                                    cellspacing="0"
                                    role="presentation"
                                    style="
                                      mso-table-lspace: 0pt;
                                      mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                  >
                                    <tr>
                                      <td
                                        class="alignment"
                                        style="
                                          vertical-align: middle;
                                          text-align: center;
                                        "
                                      >
                                        <!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
                                        <!--[if !vml]><!-->
                                        <table
                                          cellpadding="0"
                                          cellspacing="0"
                                          class="icons-inner"
                                          role="presentation"
                                          style="
                                            mso-table-lspace: 0pt;
                                            mso-table-rspace: 0pt;
                                            display: inline-block;
                                            margin-right: -4px;
                                            padding-left: 0px;
                                            padding-right: 0px;
                                          "
                                        >
                                          <!--<![endif]-->
                                          <tr>
                                            <td
                                              style="
                                                vertical-align: middle;
                                                text-align: center;
                                                padding-top: 5px;
                                                padding-bottom: 5px;
                                                padding-left: 5px;
                                                padding-right: 6px;
                                              "
                                            >
                                              <a
                                                href="https://www.designedwithbee.com/"
                                                style="text-decoration: none;"
                                                target="_blank"
                                              >
                                                <img
                                                  align="center"
                                                  alt="Designed with BEE"
                                                  class="icon"
                                                  height="32"
                                                  src="images/bee.png"
                                                  style="
                                                    display: block;
                                                    height: auto;
                                                    margin: 0 auto;
                                                    border: 0;
                                                  "
                                                  width="34"
                                                />
                                              </a>
                                            </td>
                                            <td
                                              style="
                                                font-family: Poppins, Arial,
                                                  Helvetica, sans-serif;
                                                font-size: 15px;
                                                color: #9d9d9d;
                                                vertical-align: middle;
                                                letter-spacing: undefined;
                                                text-align: center;
                                              "
                                            >
                                              <a
                                                href="https://www.designedwithbee.com/"
                                                style="
                                                  color: #9d9d9d;
                                                  text-decoration: none;
                                                "
                                                target="_blank"
                                              >
                                                Designed with BEE
                                              </a>
                                            </td>
                                          </tr>
                                        </table>
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- End -->
  </body>
</html>

    """
    return body


""" Send an email to the user with the list of new content """


def send_email(dest, list):
    user = "YOUR_MAIL"
    password = "YOUR_MAIL_PASSWORD"

    sent_from = user
    to = dest
    subject = "NEW CONTENT !!!"

    body = createHTMLbody(list)

    em = MIMEMultipart("alternative")
    em["From"] = formataddr(
        (str(Header("Movies and Series Services", "utf-8")), sent_from)
    )
    em["To"] = ", ".join(to)
    em["Subject"] = subject

    html = MIMEText(body, "html")

    em.attach(html)

    try:
        smtp_server = smtplib.SMTP_SSL("YOUR_MAIL_SERVER", YOUR_MAIL_SMTP_SERVER_PORT)
        smtp_server.ehlo()
        smtp_server.login(user, password)
        smtp_server.sendmail(sent_from, to, em.as_string())
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)


""" Retreive the content from the server """
items = retrieveMediaFromServer(protocol, server, port)

""" Get the list of series or movies """
seriesOrMovies = getSeriesOrMovies(items)

""" Create a playlist with the new content """
createOnePlaylist(items, path)

""" Send an email to the user with the list of new content """
send_email(["YOUR_ADDRESSEE_MAIL"], seriesOrMovies)
