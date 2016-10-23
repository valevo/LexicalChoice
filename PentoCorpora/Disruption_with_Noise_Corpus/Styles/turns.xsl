<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:mmax="org.eml.MMAX2.discourse.MMAX2DiscourseLoader"
                xmlns:utterances="www.eml.org/NameSpaces/utterances"
                xmlns:turns="www.eml.org/NameSpaces/turns">
  <xsl:output method="text" indent="no" omit-xml-declaration="yes"/>
<xsl:strip-space elements="*"/>

<xsl:template match="words">
 <xsl:apply-templates/>
</xsl:template>

<xsl:template match="word">
<xsl:value-of select="mmax:registerDiscourseElement(@id)"/>
<xsl:text> </xsl:text>
<xsl:apply-templates select="mmax:getStartedMarkables(@id)" mode="opening"/>
<xsl:value-of select="mmax:setStartWithAttributes()"/>
<xsl:apply-templates/>
<xsl:value-of select="mmax:setEndWithAttributes()"/>
<xsl:apply-templates select="mmax:getEndedMarkables(@id)" mode="closing"/>
</xsl:template>

<xsl:template match="turns:markable" mode="opening">
<xsl:text>
</xsl:text>
<xsl:value-of select="mmax:startBold()"/>
 <xsl:value-of select="@speaker"/>
 <xsl:text> </xsl:text>
 <xsl:value-of select="@number"/>
 <xsl:text>: </xsl:text>
<xsl:value-of select="mmax:endBold()"/>
</xsl:template>

</xsl:stylesheet>
