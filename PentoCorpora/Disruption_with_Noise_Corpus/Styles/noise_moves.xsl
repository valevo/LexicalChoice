<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:mmax="org.eml.MMAX2.discourse.MMAX2DiscourseLoader"
                xmlns:utterances="www.eml.org/NameSpaces/utterances"
                xmlns:moves="www.eml.org/NameSpaces/moves"
                xmlns:topic="www.eml.org/NameSpaces/topic"
                xmlns:turns="www.eml.org/NameSpaces/turns">
<xsl:output method="text" indent="no" omit-xml-declaration="yes"/>
<xsl:strip-space elements="*"/>

<xsl:template match="words">
 <xsl:apply-templates/>
</xsl:template>

<xsl:template match="word">
 <xsl:value-of select="mmax:registerDiscourseElement(@id)"/>
  <xsl:apply-templates select="mmax:getStartedMarkables(@id)" mode="opening"/>
   <xsl:value-of select="mmax:setDiscourseElementStart()"/>
    <xsl:apply-templates/>
   <xsl:value-of select="mmax:setDiscourseElementEnd()"/>
  <xsl:apply-templates select="mmax:getEndedMarkables(@id)" mode="closing"/>
 <xsl:text> </xsl:text>
</xsl:template>


  <xsl:template match="utterances:markable" mode="opening">
    <xsl:variable name="playbutton"><xsl:value-of select="substring(@start,1,6)"/><xsl:text> - </xsl:text><xsl:value-of select="substring(@end,1,6)"/></xsl:variable>
    <xsl:variable name="playcommand">playwavsound <xsl:value-of select="mmax:getAnnotationName()"/>.aif <xsl:value-of select="@start"/><xsl:text> </xsl:text><xsl:value-of select="@end"/></xsl:variable>
    <xsl:text>
</xsl:text>
    <xsl:value-of select="mmax:addHotSpot($playbutton, $playcommand)"/>
    <xsl:text>	</xsl:text>
    <xsl:value-of select="mmax:startBold()"/>
    <xsl:value-of select="substring(@speaker,1,3)"/>
    <xsl:text>.</xsl:text>
    <xsl:value-of select="@number"/>
    <xsl:text>:	</xsl:text>
    <xsl:value-of select="mmax:endBold()"/>
    <!--<xsl:text>	</xsl:text> <! This is a tab character -->
    <xsl:text> </xsl:text>
  </xsl:template>


<xsl:template match="utterances:markable" mode="closing">
<xsl:text>
</xsl:text>
</xsl:template>


<!-- add a newline after each topic block -->
<xsl:template match="topic:markable" mode="closing">
<xsl:text>
</xsl:text>
</xsl:template>


<!-- add a newline and an empty line after each move -->
<xsl:template match="moves:markable" mode="closing">
<xsl:text>
--------------------------------------------------------------------------------------------
</xsl:text>
</xsl:template>





</xsl:stylesheet>
