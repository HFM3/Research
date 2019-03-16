import xml.etree.ElementTree as ET


def color(hex6_color, opacity):
    """
    Converts hex color to work with KML
    :param hex6_color: hex color without "#"
    :param opacity: A value between 0 and 100. 0 = transparent
    :return: KML color string
    """
    r = hex6_color[:2]
    g = hex6_color[2:4]
    b = hex6_color[4:]
    opacity = hex(int(round(opacity / 100 * 255, 0)))[2:]
    kml_color = str(opacity + b + g + r).lower()

    return kml_color


def altitude_modes(alt_mode):
    """
    Converts abbreviated altitude mode to full length
    :param alt_mode: abbreviated altitude mode
    :return: Full altitude mode
    """
    if alt_mode == "abs":
        mode_to_use = "absolute"
    elif alt_mode == "ctg":
        mode_to_use = "clampToGround"
    elif alt_mode == "ctsf":
        mode_to_use = "clampToSeaFloor"
    elif alt_mode == "rtg":
        mode_to_use = "relativeToGround"
    elif alt_mode == "rtsf":
        mode_to_use = "relativeToSeaFloor"
    else:
        mode_to_use = "clampToGround"

    return mode_to_use


def point_style(name, icon, icon_hex6_color,
                scale=1, label_opacity=100, label_size=1, label_hex6="ffffff", icon_opacity=100):
    """
    Creates a style to be used by points within the KML
    :param name: Name of style
    :param icon: Icon url
    :param icon_hex6_color: hex color without '#'
    :param scale: Scale of icon (float)
    :param label_opacity: 0-100
    :param label_size: Scale of label (float)
    :param label_hex6: hex color without '#'
    :param icon_opacity: 0-100
    :return: an XML element as an object
    """
    style = ET.Element("Style", id=name)
    icon_style = ET.SubElement(style, "IconStyle")
    ET.SubElement(icon_style, "color").text = color(icon_hex6_color, icon_opacity)
    ET.SubElement(icon_style, "scale").text = str(scale)
    icon_icon = ET.SubElement(icon_style, "Icon")
    ET.SubElement(icon_icon, "href").text = str(icon)
    label_style = ET.SubElement(style, "LabelStyle")
    ET.SubElement(label_style, "scale").text = str(label_size)
    ET.SubElement(label_style, "color").text = color(label_hex6, label_opacity)

    return style


def line_style(name, hex_color="ff0000", width=3, opacity=100):
    """
    Creates a style to be used by lines within the KML
    :param name: Name of style
    :param hex_color: hex color without '#'
    :param width: Thickness of line (float)
    :param opacity: 0-100
    :return: an XML element as an object
    """
    style = ET.Element("Style", id=name)
    styled_line = ET.SubElement(style, "LineStyle")
    ET.SubElement(styled_line, "color").text = color(hex_color, opacity)
    ET.SubElement(styled_line, "width").text = str(width)

    return style


def polygon_style(name, poly_hex_color="00d0ff", line_hex_color="ff0050", poly_opacity=50, line_opacity=100,
                  line_width=3):
    """
    Creates a style to be used by polygons within the KML
    :param name: Name of style
    :param poly_hex_color: Polygon fill color - hex color without '#'
    :param line_hex_color: Polygon outline color - hex color without '#'
    :param poly_opacity: Fill opacity (0-100)
    :param line_opacity: Outline opacity (0-100)
    :param line_width: Thickness of outline (float)
    :return: an XML element as an object
    """
    style = ET.Element("Style", id=name)
    styled_line = ET.SubElement(style, "LineStyle")
    ET.SubElement(styled_line, "color").text = color(line_hex_color, line_opacity)
    ET.SubElement(styled_line, "width").text = str(line_width)
    poly_style = ET.SubElement(style, "PolyStyle")
    ET.SubElement(poly_style, "color").text = color(poly_hex_color, poly_opacity)

    return style


def placemarks(csv_list, folder_name, name_col_name, coord_col_names,
               altitude_mode="ctg", style_to_use=None, description=None, visibility=1):
    """
    Creates a folder of KML placemarks from a 2D list
    :param csv_list: CSV list that contains necessary fields to create a placemark (x, y, z)
    :param folder_name: Name of folder that will hold placemarks
    :param name_col_name: Name of the column that contains placemark names
    :param coord_col_names: List of x, y, z cols names : [x_col_name, y_col_name, z_col_name]
    :param altitude_mode: Abbreviated altitude mode (Optional)
    :param style_to_use: Name of point style to use (Optional)
    :param description: Description of layer (Optional)
    :param visibility: 1 = Visible, 0 = Invisible (Optional)
    :return: A folder of placemarks - an XML element as an object
    """

    x_col_name = coord_col_names[0]
    y_col_name = coord_col_names[1]
    z_col_name = coord_col_names[2]

    folder = ET.Element("Folder")
    ET.SubElement(folder, "name").text = str(folder_name)
    ET.SubElement(folder, "visibility").text = str(visibility)

    if description is not None:
        ET.SubElement(folder, "description").text = str(description)

    headers = [header for header in csv_list[0]]
    cols_to_index = [name_col_name, x_col_name, y_col_name, z_col_name]
    col_indexes = [headers.index(col) for col in cols_to_index]

    for row in csv_list[1:]:
        try:
            x = float(row[col_indexes[1]])
            y = float(row[col_indexes[2]])
            z = int(float(row[col_indexes[3]]))
        except ValueError:
            continue

        attributes = [cell for cell in row]
        attribute_str = "<![CDATA["

        for cell in range(len(headers)):
            attribute_str += "<b>" + str(headers[cell]) + "</b>: " + str(attributes[cell]) + "<br>"
        attribute_str += "]]>"

        placemark = ET.SubElement(folder, "Placemark")
        ET.SubElement(placemark, "name").text = row[col_indexes[0]]
        ET.SubElement(placemark, "visibility").text = str(visibility)
        ET.SubElement(placemark, "description").text = attribute_str
        if style_to_use is not None:
            ET.SubElement(placemark, "styleUrl").text = style_to_use
        point = ET.SubElement(placemark, "Point")
        ET.SubElement(point, "coordinates").text = str(x) + "," + str(y) + "," + str(z)
        ET.SubElement(point, "altitudeMode").text = altitude_modes(altitude_mode)

        extended_data = ET.SubElement(placemark, "ExtendedData")

        for cell in range(len(headers)):
            data = ET.SubElement(extended_data, "Data", name=str(headers[cell]))
            ET.SubElement(data, "displayName").text = str(headers[cell])
            ET.SubElement(data, "value").text = str(row[cell])

    return folder


def two_point_line(csv_list, folder_name, name_col_name, coord_col_names, altitude_mode="ctg", style_to_use=None,
                   description=None, visibility=1, draw_order=0):
    """
    Creates a folder of KML lines from a 2D list
    :param csv_list: CSV list that contains necessary fields to create a two point line (x, y, z) x2
    :param folder_name: Name of folder that will hold lines
    :param name_col_name: Name of the column that contains line names
    :param coord_col_names: A list of col names : [x1_col_name, y1_col_name, z1_col_name, x2_col_name, y2_col_name, z2_col_name]
    :param altitude_mode: Abbreviated altitude mode (Optional)
    :param style_to_use: Name of line style to use (Optional)
    :param description: Description of layer (Optional)
    :param visibility: 1 = Visible, 0 = Invisible (Optional)
    :param draw_order: order of rendering (Higher values render first)
    :return: A folder of lines - an XML element as an object
    """
    # coord_col_names =
    x1_col_name = coord_col_names[0]
    y1_col_name = coord_col_names[1]
    z1_col_name = coord_col_names[2]

    x2_col_name = coord_col_names[3]
    y2_col_name = coord_col_names[4]
    z2_col_name = coord_col_names[5]

    folder = ET.Element("Folder")
    ET.SubElement(folder, "name").text = str(folder_name)
    ET.SubElement(folder, "visibility").text = str(visibility)

    if description is not None:
        ET.SubElement(folder, "description").text = str(description)

    headers = [header for header in csv_list[0]]
    cols_to_index = [name_col_name, x1_col_name, y1_col_name, z1_col_name, x2_col_name, y2_col_name, z2_col_name]
    col_indexes = [csv_list[0].index(col) for col in cols_to_index]
    # headers.append("Distance (m)")

    for row in csv_list[1:]:
        try:
            x1 = float(row[col_indexes[1]])
            y1 = float(row[col_indexes[2]])
            z1 = int(float(row[col_indexes[3]]))
            x2 = float(row[col_indexes[4]])
            y2 = float(row[col_indexes[5]])
            z2 = int(float(row[col_indexes[6]]))
        except (ValueError, IndexError):
            continue

        attributes = [cell for cell in row]
        attribute_str = "<![CDATA["
        for cell in range(len(headers)):
            attribute_str += "<b>" + str(headers[cell]) + "</b>: " + str(attributes[cell]) + "<br>"
        attribute_str += "]]>"

        placemark = ET.SubElement(folder, "Placemark")
        ET.SubElement(placemark, "name").text = row[col_indexes[0]]
        ET.SubElement(placemark, "visibility").text = str(visibility)
        ET.SubElement(placemark, "description").text = attribute_str
        ET.SubElement(placemark, "gx:drawOrder").text = str(draw_order)
        if style_to_use is not None:
            ET.SubElement(placemark, "styleUrl").text = style_to_use
        else:
            style = ET.SubElement(placemark, "Style")
            styled_line = ET.SubElement(style, "LineStyle")
            ET.SubElement(styled_line, "color").text = "ff0000ff"
            ET.SubElement(styled_line, "width").text = "2"

        line = ET.SubElement(placemark, "LineString")

        coord_str1 = str(x1) + "," + str(y1) + "," + str(z1)
        coord_str2 = str(x2) + "," + str(y2) + "," + str(z2)
        ET.SubElement(line, "coordinates").text = coord_str1 + " " + coord_str2
        ET.SubElement(line, "altitudeMode").text = altitude_modes(altitude_mode)

        extended_data = ET.SubElement(placemark, "ExtendedData")

        for cell in range(len(headers)):
            data = ET.SubElement(extended_data, "Data", name=str(headers[cell]))
            ET.SubElement(data, "displayName").text = str(headers[cell])
            ET.SubElement(data, "value").text = str(row[cell])

    return folder


def solid_polygon(folder_name, poly_coords, attributes, name_col_name=None,
                  altitude_mode="ctg", style_to_use=None, visibility=1):
    """
    Creates a folder of solid KML polygons. Does not create polygons with holes
    :param folder_name: Name of folder that will hold polygons
    :param poly_coords: [[[x y, z], [x y, z], [x y, z]], [poly 2], [poly 3]
    :param attributes: [[Poly 1 Attributes], [Poly 2 Attributes]]
    :param name_col_name: Name of the column that contains polygon names
    :param altitude_mode: Abbreviated altitude mode (Optional)
    :param style_to_use: Name of polygon style to use (Optional)
    :param visibility: 1 = Visible, 0 = Invisible (Optional)
    :return: A folder of polygons - an XML element as an object
    """

    outer_poly_coords = poly_coords

    folder = ET.Element("Folder")
    ET.SubElement(folder, "name").text = str(folder_name)
    ET.SubElement(folder, "visibility").text = str(visibility)

    headers = [header for header in attributes[0]]
    name_col_index = headers.index(name_col_name)
    cdata_list = []
    extended_data_list = []

    for row in attributes[1:]:
        row_attributes = [cell for cell in row]
        # print(attributes)
        attribute_str = "<![CDATA["

        for cell in range(len(headers)):
            attribute_str += "<b>" + str(headers[cell]) + "</b>: " + str(row_attributes[cell]) + "<br>"
        attribute_str += "]]>"

        cdata_list.append(attribute_str)

        extended_data = ET.Element("ExtendedData")
        for cell in range(len(headers)):
            data = ET.SubElement(extended_data, "Data", name=str(headers[cell]))
            ET.SubElement(data, "displayName").text = str(headers[cell])
            ET.SubElement(data, "value").text = str(row[cell])
        extended_data_list.append(extended_data)

    count = 0
    for outer_poly in outer_poly_coords:
        outer_boundary_coord_str = ""
        for coord_set in outer_poly:
            try:
                x = float(coord_set[0])
                y = float(coord_set[1])
                z = int(float(coord_set[2]))

                outer_boundary_coord_str += str(x) + "," + str(y) + "," + str(z) + " "
            except ValueError:
                pass
        first_coord = outer_boundary_coord_str[:outer_boundary_coord_str.index(" ")]
        outer_boundary_coord_str += first_coord

        placemark = ET.SubElement(folder, "Placemark")
        ET.SubElement(placemark, "name").text = str(attributes[count + 1][name_col_index])
        ET.SubElement(placemark, "visibility").text = str(visibility)
        ET.SubElement(placemark, "description").text = cdata_list[count]
        if style_to_use is not None:
            ET.SubElement(placemark, "styleUrl").text = style_to_use
        polygon = ET.SubElement(placemark, "Polygon")

        outer_boundary = ET.SubElement(polygon, "outerBoundaryIs")
        outer_linear_ring = ET.SubElement(outer_boundary, "LinearRing")
        ET.SubElement(outer_linear_ring, "coordinates").text = outer_boundary_coord_str

        ET.SubElement(polygon, "altitudeMode").text = altitude_modes(altitude_mode)
        placemark.append(extended_data_list[count])

        count += 1

    return folder


def folder_gather(name, sub_folders):
    """
    Moves KML folders to a new parent folder
    :param name: Name of folder that will hold sub-folders
    :param sub_folders: list of folders [folder 1, folder 2]
    :return: new folder - an XML element as an object
    """
    new_folder = ET.Element("Folder")
    ET.SubElement(new_folder, "name").text = str(name)
    for sub_folder in sub_folders:
        ET.Element.append(new_folder, sub_folder)
    return new_folder


def doc_setup(name, description=None):
    """
    Creates and KML document for styles and placemarks, lines, and polygons to be added to.
    :param name: Name of KML document, not KML file. Name will appear when KML is opened.
    :param description: Optional. Will appear below Name when opened.
    :return: XML object of KML document
    """
    kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(kml, "Document")
    ET.SubElement(doc, "name").text = name
    if description is not None:
        print("not None")
        ET.SubElement(doc, "description").text = str(description)
    return kml


def kml_build(doc, styles, folders):
    """
    Brings KML elements together as a KML doc
    :param doc: KML do to add styles and folders of elements to
    :param styles: A list of styles to include
    :param folders: A list of folders of elements to include
    :return: KML as a string
    """
    whole_doc = ET.ElementTree(doc).getroot()
    xml_doc = whole_doc[0]
    # print(str(ET.tostring(whole_doc[0]), 'utf-8'))
    for style in styles:
        ET.Element.append(xml_doc, style)
    for each in folders:
        ET.Element.append(xml_doc, each)

    kml_str = str(ET.tostring(whole_doc), 'utf-8')

    # replacements to fix CDATA XML escaped characters
    # counts <![CDATA[]]> occurrences
    last_found = -1
    cdata = []
    while True:
        last_found = kml_str.find("&lt;![CDATA[", last_found + 1)
        if last_found == -1:
            break
        cdata.append(last_found)

    cdata_count = len(cdata)

    # Replaces XML escaped characters in <![CDATA[]]>
    for x in range(0, cdata_count):
        cdata_start = kml_str.find("&lt;![CDATA[")
        cdata_end = kml_str.find("]]&gt;") + len("]]&gt;")

        str_1 = kml_str[:cdata_start]
        str_2 = kml_str[cdata_end:]
        substring = kml_str[cdata_start:cdata_end]

        substring = substring.replace("&lt;", "<")
        substring = substring.replace("&gt;", ">")
        substring = substring.replace("&amp;", "&")
        substring = substring.replace("&quot;", '"')
        substring = substring.replace("&apos;", "'")

        kml_str = str_1 + substring + str_2

    return kml_str

