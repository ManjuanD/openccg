<!--Copyright (C) 2005-2009 Scott Martin, Rajakrishan Rajkumar and Michael White
 
 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.
 
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.
 
 You should have received a copy of the GNU Lesser General Public
 License along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.-->


<xsl:transform
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0"
  xmlns:xalan="http://xml.apache.org/xalan"
  xmlns:xalan2="http://xml.apache.org/xslt"
  xmlns:java="http://xml.apache.org/xalan/java"
  exclude-result-prefixes="xalan xalan2 java">

<xsl:output method="xml" indent="yes" xalan2:indent-amount="2" omit-xml-declaration = "yes"/>

<xsl:strip-space elements="*"/>

<!--Transform which inserts orig punct cats i.e cats akin to binary rules-->

<xsl:template match="/">
 	<xsl:apply-templates/>
</xsl:template>

<!--Add *NoSem indexRel to punctuation cats except conj commas-->
<xsl:template match="family[@pos1='PUNCT' and not(@pos='PUNCT_CONJ')]">
	<family>
		<xsl:attribute name="indexRel">*NoSem*</xsl:attribute>
		<xsl:apply-templates select="@*|node()"/>
	</family>
</xsl:template>

<!--Strip off semantics conferred by default templates-->
<xsl:template match="lf[ancestor::family[@pos1='PUNCT' and not(@pos='PUNCT_CONJ')]]"/>
<xsl:template match="feat[(@attr='index' or @attr='mod-index') and ancestor::family[@pos1='PUNCT' and not(@pos='PUNCT_CONJ')]]"/>

<!--Default global copy rule-->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:transform>