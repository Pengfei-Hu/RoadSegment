define({"oj-message":{fatal:"Kritik",error:"Hata",warning:"Uyarı",info:"Bilgiler",confirmation:"Teyit","compact-type-summary":"{0}: {1}"},"oj-converter":{summary:"Değer beklenen formatta değil.",detail:"Beklenen formatta bir değer girin.","plural-separator":", ",hint:{summary:"Örnek: {exampleValue}",detail:"Şu formatta bir değer girin: '{exampleValue}'.","detail-plural":"Şu formatlarda bir değer girin: '{exampleValue}'."},optionHint:{detail:"'{propertyValueValid}', '{propertyName}' seçeneği için kabul edilen bir değerdir.","detail-plural":"'{propertyValueValid}', '{propertyName}' seçeneği için kabul edilen değerlerdir."},optionTypesMismatch:{summary:"'{propertyName}' seçeneği '{propertyValue}' 'olarak ayarlandığında, {requiredPropertyName}' seçeneği için bir değer gereklidir."},optionTypeInvalid:{summary:"'{propertyName}' seçeneği için beklenen türde bir değer sağlanmadı."},optionOutOfRange:{summary:"'{propertyName}' seçeneği için {propertyValue} değeri aralığın dışında."},optionValueInvalid:{summary:"'{propertyName}' seçeneği için geçersiz '{propertyValue}' değeri belirtildi."},number:{decimalFormatMismatch:{summary:"Sağlanan değer, beklenen sayı formatında değil."},shortLongUnsupportedParse:{summary:"'short' ve 'long' dönüştürücü ayrıştırmada desteklenmez.",detail:"Bileşeni readonly olarak değiştirin. readonly alanları dönüştürücünün ayrıştırma fonksiyonunu çağırmaz."},currencyFormatMismatch:{summary:"Sağlanan değer, beklenen para birimi formatında değil."},percentFormatMismatch:{summary:"Sağlanan değer, beklenen yüzde formatında değil."},invalidNumberFormat:{summary:"Sağlanan değer geçerli bir sayı değil.",detail:"Lütfen geçerli bir sayı belirtin."}},color:{invalidFormat:{summary:"Geçersiz renk formatı.",detail:"Geçersiz renk formatı seçeneği belirtimi."},invalidSyntax:{summary:"Geçersiz renk belirtimi.",detail:"CSS3 standardına uyan bir renk değeri girin."}},datetime:{datetimeOutOfRange:{summary:"'{propertyName}' için '{value}' değeri aralığın dışında.",detail:"'{minValue}' ile '{maxValue}' arasında bir değer girin.",hour:"saat",minute:"dakika",second:"saniye",millisec:"milisaniye",month:"ay",day:"gün",year:"yıl","month name":"ay adı",weekday:"hafta içi gün"},dateFormatMismatch:{summary:"Sağlanan değer, beklenen tarih formatında değil."},invalidTimeZoneID:{summary:"Geçersiz saat dilimi no {timeZoneID} sağlandı."},nonExistingTime:{summary:"Girdi saati yok çünkü gün ışığından yararlanma saatine geçişe rastlıyor."},missingTimeZoneData:{summary:"Saat Dilimi verisi yok. Saat Dilimi verisini yüklemek için lütfen 'ojs/ojtimezonedata' gereklidir."},timeFormatMismatch:{summary:"Sağlanan değer, beklenen saat formatında değil."},datetimeFormatMismatch:{summary:"Sağlanan değer, beklenen tarih ve saat formatında değil."},dateToWeekdayMismatch:{summary:"'{date}' tarihi '{weekday}' gününe denk gelmiyor.",detail:"Tarihe karşılık gelen bir gün girin."},invalidISOString:{invalidRangeSummary:"'{value}' değeri, '{isoStr}' ISO 8601 dizesindeki {propertyName} alanı için aralığın dışında.",summary:"Sağlanan '{isoStr}' geçerli bir ISO 8601 dizesi değil.",detail:"Lütfen geçerli ISO 8601 dizesi sağlayın."}}},"oj-validator":{length:{hint:{min:"{min} veya daha fazla karakter girin.",max:"{max} veya daha az karakter girin.",inRange:"{min} ila {max} karakter girin.",exact:"{length} karakter girin."},messageDetail:{tooShort:"{min} veya daha fazla karakter girin.",tooLong:"En fazla {max} karakter girin."},messageSummary:{tooShort:"Çok az karakter var.",tooLong:"Çok fazla karakter var."}},range:{number:{hint:{min:"{min} değerine eşit veya daha büyük bir sayı girin.",max:"{max} değerine eşit veya daha küçük bir sayı girin.",inRange:"{min} ve {max} arasında bir sayı girin.",exact:"{num} sayısını girin."},messageDetail:{rangeUnderflow:"{min} veya daha büyük bir sayı girin.",rangeOverflow:"{max} veya daha küçük bir sayı girin.",exact:"{num} sayısını girin."},messageSummary:{rangeUnderflow:"Sayı çok küçük.",rangeOverflow:"Sayı çok büyük."}},datetime:{hint:{min:"{min} ile eşit veya daha sonra olan bir tarih ve saat girin.",max:"{max} ile eşit veya daha önce olan bir tarih ve saat girin.",inRange:"{min} ve {max} arasında bir tarih ve saat girin."},messageDetail:{rangeUnderflow:"{min} tarihine eşit veya bundan sonra olan bir tarih girin.",rangeOverflow:"{max} tarihine eşit veya bundan önce olan bir tarih girin."},messageSummary:{rangeUnderflow:"Tarih ve saat minimum tarih ve saatten önce.",rangeOverflow:"Tarih ve saat maksimum tarih ve saatten sonra olmalıdır."}},date:{hint:{min:"{min} tarihine eşit veya bundan sonra olan bir tarih girin.",max:"{max} tarihine eşit veya bundan önce olan bir tarih girin.",inRange:"{min} ile {max} arasında bir tarih girin."},messageDetail:{rangeUnderflow:"{min} tarihine eşit veya bundan sonra olan bir tarih girin.",rangeOverflow:"{max} tarihine eşit veya bundan önce olan bir tarih girin."},messageSummary:{rangeUnderflow:"Tarih minimum tarihten önce.",rangeOverflow:"Tarih maksimum tarihten sonra."}},time:{hint:{min:"{min} saatine eşit veya bundan sonra olan bir saat girin.",max:"{max} saatine eşit veya bundan önce olan bir tarih girin.",inRange:"{min} ile {max} arasında bir saat girin."},messageDetail:{rangeUnderflow:"{min} saatine eşit veya bundan sonra olan bir saat girin.",rangeOverflow:"{max} saatine eşit veya bundan önce olan bir saat girin."},messageSummary:{rangeUnderflow:"Saat minimum saatten önce.",rangeOverflow:"Saat maksimum saatten sonra."}}},restriction:{date:{messageSummary:"{value} tarihi devre dışı bırakılmış bir girişe ait.",messageDetail:"Seçtiğiniz tarih kullanılamıyor. Başka bir tarih deneyin."}},regExp:{summary:"Format yanlış",detail:"Şu düzenli ifadede açıklanan izin verilebilir değerleri girin: '{pattern}'."},required:{summary:"Değer gereklidir.",detail:"Bir değer girin."}},"oj-ojEditableValue":{loading:"Yükleniyor",requiredText:"Gerekli",helpSourceText:"Daha fazla bilgi edinin..."},"oj-ojInputDate":{done:"Bitti",cancel:"İptal",prevText:"Geri",nextText:"İleri",currentText:"Bugün",weekHeader:"Hft",tooltipCalendar:"Tarih Seç.",tooltipCalendarTime:"Tarih/Saat Seç.",tooltipCalendarDisabled:"Tarih Seçme Devre Dışı.",tooltipCalendarTimeDisabled:"Tarih/Saat Seçme Devre Dışı.",picker:"Seçici",weekText:"Hafta",datePicker:"Tarih Seçici",inputHelp:"Takvime erişmek için Aşağı tuşuna veya Yukarı tuşuna basın.",inputHelpBoth:"Takvime erişmek için Aşağı tuşuna veya Yukarı tuşuna basın ve saat açılır menüsüne erişmek için Shift + Aşağı tuşuna veya Shift + Yukarı tuşuna basın.",dateTimeRange:{hint:{min:"",max:"",inRange:""},messageDetail:{rangeUnderflow:"",rangeOverflow:""},messageSummary:{rangeUnderflow:"",rangeOverflow:""}},dateRestriction:{hint:"",messageSummary:"",messageDetail:""}},"oj-ojInputTime":{cancelText:"İptal",okText:"Tamam",currentTimeText:"Şimdi",hourWheelLabel:"Saat",minuteWheelLabel:"Dakika",ampmWheelLabel:"ÖÖÖS",tooltipTime:"Saat Seç.",tooltipTimeDisabled:"Saat Seçme Devre Dışı.",inputHelp:"Saat açılır menüsüne erişmek için Aşağı tuşuna veya Yukarı tuşuna basın.",dateTimeRange:{hint:{min:"",max:"",inRange:""},messageDetail:{rangeUnderflow:"",rangeOverflow:""},messageSummary:{rangeUnderflow:"",rangeOverflow:""}}},"oj-inputBase":{required:{hint:"",messageSummary:"",messageDetail:""},regexp:{messageSummary:"",messageDetail:""},accessibleMaxLengthExceeded:"Maksimum uzunluk {len} aşıldı.",accessibleMaxLengthRemaining:"{chars} karakter kaldı."},"oj-ojInputPassword":{regexp:{messageDetail:"Değer bu düzenle eşleşmelidir: '{pattern}'."},accessibleShowPassword:"Parolayı göster.",accessibleHidePassword:"Parolayı gizle."},"oj-ojFilmStrip":{labelAccFilmStrip:"{pageIndex} / {pageCount} sayfa görüntüleniyor",labelAccArrowNextPage:"Sonraki sayfayı görüntülemek için İleri'yi seçin.",labelAccArrowPreviousPage:"Önceki sayfayı görüntülemek için Önceki'yi seçin.",tipArrowNextPage:"İleri",tipArrowPreviousPage:"Geri"},"oj-ojDataGrid":{accessibleSortAscending:"{id} artan düzende sıralanıyor",accessibleSortDescending:"{id} azalan düzende sıralanıyor",accessibleActionableMode:"İşlem yapılabilir moda geç.",accessibleNavigationMode:"Gezinme moduna geçin, F2 tuşuna basarak düzenleme moduna veya işlem yapılabilir moda geçin.",accessibleEditableMode:"Düzenlenebilir moda geçin, escape tuşuna basarak veri tablosunun dışında gezinin.",accessibleSummaryExact:"Bu, {rownum} satıra ve {colnum} sütuna sahip bir veri tablosudur",accessibleSummaryEstimate:"Bu, bilinmeyen sayıda sütuna ve satıra sahip bir veri tablosudur",accessibleSummaryExpanded:"Şu anda {num} satır genişletildi",accessibleRowExpanded:"Satır genişletildi",accessibleRowCollapsed:"Satır daraltıldı",accessibleRowSelected:"{row} numaralı satır seçildi",accessibleColumnSelected:"{column} numaralı sütun seçildi",accessibleStateSelected:"seçildi",accessibleMultiCellSelected:"{num} hücre seçildi",accessibleColumnSpanContext:"{extent} geniş",accessibleRowSpanContext:"{extent} yüksek",accessibleRowContext:"Satır {index}",accessibleColumnContext:"Sütun {index}",accessibleRowHeaderContext:"Satır Başlığı {index}",accessibleColumnHeaderContext:"Sütun Başlığı {index}",accessibleRowEndHeaderContext:"Satır Sonu Başlığı {index}",accessibleColumnEndHeaderContext:"Sütun Sonu Başlığı {index}",accessibleRowHeaderLabelContext:"Satır Başlığı Etiketi {level}",accessibleColumnHeaderLabelContext:"Sütun Başlığı Etiketi {level}",accessibleRowEndHeaderLabelContext:"Satır Sonu Başlığı Etiketi {level}",accessibleColumnEndHeaderLabelContext:"Sütun Sonu Başlığı Etiketi {level}",accessibleLevelContext:"Düzey {level}",accessibleRangeSelectModeOn:"Seçili hücre aralığı ekleme modu açık.",accessibleRangeSelectModeOff:"Seçili hücre aralığı ekleme modu kapalı.",accessibleFirstRow:"İlk satıra ulaştınız.",accessibleLastRow:"Son satıra ulaştınız.",accessibleFirstColumn:"İlk sütuna ulaştınız",accessibleLastColumn:"Son sütuna ulaştınız.",accessibleSelectionAffordanceTop:"Üst seçim tutamacı.",accessibleSelectionAffordanceBottom:"Alt seçim tutamacı.",msgFetchingData:"Veriler Alınıyor...",msgNoData:"Görüntülenecek öğe yok.",labelResize:"Yeniden Boyutlandır",labelResizeWidth:"Yeniden Boyutlandırma Genişliği",labelResizeHeight:"Yeniden Boyutlandırma Yüksekliği",labelSortRow:"Satırı Sırala",labelSortRowAsc:"Satırı Artan Düzende Sırala",labelSortRowDsc:"Satırı Azalan Düzende Sırala",labelSortCol:"Sütunu Sırala",labelSortColAsc:"Sütunu Artan Düzende Sırala",labelSortColDsc:"Sütunu Azalan Düzende Sırala",labelCut:"Kes",labelPaste:"Yapıştır",labelEnableNonContiguous:"Bitişik Olmayan Seçimi Etkinleştir",labelDisableNonContiguous:"Bitişik Olmayan Seçimi Devre Dışı Bırak",labelResizeDialogSubmit:"Tamam",labelResizeDialogCancel:"İptal",accessibleContainsControls:"Denetimler İçerir"},"oj-ojRowExpander":{accessibleLevelDescription:"Düzey {level}",accessibleRowDescription:"Düzey {level}, {num} / {total} Satır",accessibleRowExpanded:"Satır genişletildi",accessibleRowCollapsed:"Satır daraltıldı",accessibleStateExpanded:"genişletildi",accessibleStateCollapsed:"daraltıldı"},"oj-ojListView":{msgFetchingData:"Veriler Alınıyor...",msgNoData:"Görüntülenecek öğe yok.",msgItemsAppended:"{count} öğe sona eklendi.",indexerCharacters:"A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z",accessibleReorderTouchInstructionText:"Çift dokunup basılı tutun. Sesi duyduğunuzda yeniden düzenlemek için sürükleyin.",accessibleReorderBeforeItem:"{item} öncesinde",accessibleReorderAfterItem:"{item} sonrasında",accessibleReorderInsideItem:"İçine {item}",accessibleNavigateSkipItems:"{numSkip} öğe atlanıyor",labelCut:"Kes",labelCopy:"Kopyala",labelPaste:"Yapıştır",labelPasteBefore:"Öncesine Yapıştır",labelPasteAfter:"Sonrasına Yapıştır"},"oj-_ojLabel":{tooltipHelp:"Yardım",tooltipRequired:"Gerekli"},"oj-ojLabel":{tooltipHelp:"Yardım",tooltipRequired:"Gerekli"},"oj-ojInputNumber":{required:{hint:"",messageSummary:"",messageDetail:""},numberRange:{hint:{min:"",max:"",inRange:"",exact:""},messageDetail:{rangeUnderflow:"",rangeOverflow:"",exact:""},messageSummary:{rangeUnderflow:"",rangeOverflow:""}},tooltipDecrement:"Azalma",tooltipIncrement:"Artış"},"oj-ojTable":{accessibleColumnContext:"Sütun {index}",accessibleColumnFooterContext:"Sütun Altbilgisi {index}",accessibleColumnHeaderContext:"Sütun Başlığı {index}",accessibleRowContext:"Satır {index}",accessibleSortable:"{id} sıralanabilir",accessibleSortAscending:"{id} artan düzende sıralanıyor",accessibleSortDescending:"{id} azalan düzende sıralanıyor",accessibleStateSelected:"seçildi",labelAccSelectionAffordanceTop:"Üst seçim tutamacı",labelAccSelectionAffordanceBottom:"Alt seçim tutamacı",labelEnableNonContiguousSelection:"Bitişik Olmayan Seçimi Etkinleştir",labelDisableNonContiguousSelection:"Bitişik Olmayan Seçimi Devre Dışı Bırak",labelResize:"Yeniden Boyutlandır",labelResizePopupSubmit:"Tamam",labelResizePopupCancel:"İptal",labelResizePopupSpinner:"Sütunu Yeniden Boyutlandır",labelSelectRow:"Satır Seç",labelEditRow:"Satırı Düzenle",labelSelectAndEditRow:"Satır Seç ve Düzenle",labelSelectColumn:"Sütun Seç",labelSort:"Sırala",labelSortAsc:"Artan Düzende Sırala",labelSortDsc:"Azalan Düzende Sırala",msgFetchingData:"Veriler Alınıyor...",msgNoData:"Görüntülenecek veri yok.",msgInitializing:"Başlatılıyor...",msgColumnResizeWidthValidation:"Genişlik değeri bir tamsayı olmalıdır.",msgScrollPolicyMaxCountSummary:"Tablo kaydırmak için gereken maksimum satır sayısı aşıldı.",msgScrollPolicyMaxCountDetail:"Lütfen daha küçük bir veri kümesi ile yeniden yükleyin.",msgStatusSortAscending:"{0} artan düzende sıralanıyor.",msgStatusSortDescending:"{0} azalan düzende sıralanıyor."},"oj-ojTabs":{labelCut:"Kes",labelPasteBefore:"Öncesine Yapıştır",labelPasteAfter:"Sonrasına Yapıştır",labelRemove:"Kaldır",labelReorder:"Yeniden Sırala",removeCueText:"Kaldırılabilir"},"oj-ojCheckboxset":{readonlyNoValue:"",required:{hint:"",messageSummary:"",messageDetail:""}},"oj-ojRadioset":{readonlyNoValue:"",required:{hint:"",messageSummary:"",messageDetail:""}},"oj-ojSelect":{required:{hint:"",messageSummary:"",messageDetail:""},searchField:"Arama alanı",noMatchesFound:"Eşleşme bulunmadı",oneMatchesFound:"Bir eşleşme bulundu",moreMatchesFound:"{num} eşleşme bulundu",filterFurther:"Daha fazla sonuç için lütfen filtreleyin."},"oj-ojSwitch":{SwitchON:"Açık",SwitchOFF:"Kapalı"},"oj-ojCombobox":{required:{hint:"",messageSummary:"",messageDetail:""},noMatchesFound:"Eşleşme bulunmadı",oneMatchesFound:"Bir eşleşme bulundu",moreMatchesFound:"{num} eşleşme bulundu",filterFurther:"Daha fazla sonuç için lütfen filtreleyin."},"oj-ojSelectSingle":{required:{hint:"",messageSummary:"",messageDetail:""},noMatchesFound:"Eşleşme bulunmadı",oneMatchFound:"Bir eşleşme bulundu",multipleMatchesFound:"{num} eşleşme bulundu",nOrMoreMatchesFound:"{num} veya daha fazla eşleşme bulundu.",cancel:"İptal",labelAccOpenDropdown:"genişlet",labelAccClearValue:"değeri temizle",noResultsLine1:"Sonuç bulunamadı",noResultsLine2:"Aramanızla eşleşen bir şey bulamadık."},"oj-ojInputSearch":{required:{hint:"",messageSummary:"",messageDetail:""},noMatchesFound:"Eşleşme bulunmadı",oneMatchesFound:"Bir eşleşme bulundu",moreMatchesFound:"{num} eşleşme bulundu"},"oj-ojTree":{stateLoading:"Yükleniyor...",labelNewNode:"Yeni Düğüm",labelMultiSelection:"Birden Çok Seçim",labelEdit:"Düzenle",labelCreate:"Oluştur",labelCut:"Kes",labelCopy:"Kopyala",labelPaste:"Yapıştır",labelPasteAfter:"Sonrasına Yapıştır",labelPasteBefore:"Öncesine Yapıştır",labelRemove:"Kaldır",labelRename:"Yeniden Adlandır",labelNoData:"Veri yok"},"oj-ojPagingControl":{labelAccPaging:"Sayfa Numaralandırma",labelAccPageNumber:"Sayfa {pageNum} içeriği yüklendi",labelAccNavFirstPage:"İlk Sayfa",labelAccNavLastPage:"Son Sayfa",labelAccNavNextPage:"Sonraki Sayfa",labelAccNavPreviousPage:"Önceki Sayfa",labelAccNavPage:"Sayfa",labelLoadMore:"Daha Fazla Göster...",labelLoadMoreMaxRows:"Maksimum sınır olan {maxRows} satıra ulaşıldı",labelNavInputPage:"Sayfa",labelNavInputPageMax:"/ {pageMax}",fullMsgItemRange:"{pageMax} öğeden {pageFrom}-{pageTo} tanesi",fullMsgItemRangeAtLeast:"En az {pageMax} öğeden {pageFrom}-{pageTo} tanesi",fullMsgItemRangeApprox:"Yaklaşık {pageMax} öğeden {pageFrom}-{pageTo} tanesi",msgItemRangeNoTotal:"{pageFrom}-{pageTo} öğe",fullMsgItem:"{pageMax} öğeden {pageTo} tanesi",fullMsgItemAtLeast:"En az {pageMax} öğeden {pageTo} tanesi",fullMsgItemApprox:"Yaklaşık {pageMax} öğeden {pageTo} tanesi",msgItemNoTotal:"{pageTo} öğe",msgItemRangeCurrent:"{pageFrom}-{pageTo}",msgItemRangeCurrentSingle:"{pageFrom}",msgItemRangeOf:"/",msgItemRangeOfAtLeast:"/ en az",msgItemRangeOfApprox:"/ yaklaşık",msgItemRangeItems:"öğe",tipNavInputPage:"Sayfaya Git",tipNavPageLink:"{pageNum}. Sayfaya Git",tipNavNextPage:"İleri",tipNavPreviousPage:"Geri",tipNavFirstPage:"İlk",tipNavLastPage:"Son",pageInvalid:{summary:"Girilen sayfa değeri geçersiz.",detail:"Lütfen 0'dan büyük bir değer girin."},maxPageLinksInvalid:{summary:"maxPageLinks değeri geçersiz.",detail:"Lütfen 4'ten büyük bir değer girin."}},"oj-ojMasonryLayout":{labelCut:"Kes",labelPasteBefore:"Öncesine Yapıştır",labelPasteAfter:"Sonrasına Yapıştır"},"oj-panel":{labelAccButtonExpand:"Genişlet",labelAccButtonCollapse:"Daralt",labelAccButtonRemove:"Kaldır",labelAccFlipForward:"Öne çevir",labelAccFlipBack:"Arkaya çevir",tipDragToReorder:"Yeniden sıralamak için sürükleyin",labelAccDragToReorder:"Yeniden sıralamak için çekin, bağlam menüsü mevcut"},"oj-ojChart":{labelDefaultGroupName:"Grup {0}",labelSeries:"Seri",labelGroup:"Grup",labelDate:"Tarih",labelValue:"Değer",labelTargetValue:"Hedef",labelX:"X",labelY:"Y",labelZ:"Z",labelPercentage:"Yüzde Oranı",labelLow:"Düşük",labelHigh:"Yüksek",labelOpen:"Aç",labelClose:"Kapat",labelVolume:"Hacim",labelQ1:"Q1",labelQ2:"Q2",labelQ3:"Q3",labelMin:"Minimum",labelMax:"Maksimum",labelOther:"Diğer",tooltipPan:"Kaydır",tooltipSelect:"Çerçeve seçimi",tooltipZoom:"Çerçeve yakınlaştırma",componentName:"Grafik"},"oj-dvtBaseGauge":{componentName:"Gösterge"},"oj-ojDiagram":{promotedLink:"{0} bağlantı",promotedLinks:"{0} bağlantı",promotedLinkAriaDesc:"Dolaylı",componentName:"Diyagram"},"oj-ojGantt":{componentName:"Gantt",accessibleDurationDays:"{0} gün",accessibleDurationHours:"{0} saat",accessibleTaskInfo:"Başlangıç saati {0}, bitiş saati {1}, süre {2}",accessibleMilestoneInfo:"Zaman {0}",accessibleRowInfo:"Satır {0}",accessibleTaskTypeMilestone:"Kilometre Taşı",accessibleTaskTypeSummary:"Özet",accessiblePredecessorInfo:"{0} öncül",accessibleSuccessorInfo:"{0} ardıl",accessibleDependencyInfo:"Bağımlılık tipi {0}, {1} öğesini {2} öğesine bağlar",startStartDependencyAriaDesc:"başlangıç - başlangıç",startFinishDependencyAriaDesc:"başlangıç - bitiş",finishStartDependencyAriaDesc:"bitiş - başlangıç",finishFinishDependencyAriaDesc:"bitiş - bitiş",tooltipZoomIn:"Yakınlaştır",tooltipZoomOut:"Uzaklaştır",labelLevel:"Düzey",labelRow:"Satır",labelStart:"Başlangıç",labelEnd:"Bitiş",labelDate:"Tarih",labelBaselineStart:"Referans Başlangıç",labelBaselineEnd:"Referans Bitiş",labelBaselineDate:"Referans Tarih",labelLabel:"Etiket",labelProgress:"İlerleme",labelMoveBy:"Taşıma Son Tarihi",labelResizeBy:"Yeniden Boyutlandırma Ölçütü",taskMoveInitiated:"Görev taşıma başlatıldı",taskResizeEndInitiated:"Görev yeniden boyutlandırma sonu başlatıldı",taskResizeStartInitiated:"Görev yeniden boyutlandırma başlangıcı başlatıldı",taskMoveSelectionInfo:"Başka {0} seçildi",taskResizeSelectionInfo:"Başka {0} seçildi",taskMoveInitiatedInstruction:"Taşımak için ok tuşlarını kullanın",taskResizeInitiatedInstruction:"Yeniden boyutlandırmak için ok tuşlarını kullanın",taskMoveFinalized:"Görev taşıma bitirildi",taskResizeFinalized:"Görev yeniden boyutlandırma bitirildi",taskMoveCancelled:"Görev taşıma iptal edildi",taskResizeCancelled:"Görev yeniden boyutlandırma iptal edildi",taskResizeStartHandle:"Görev yeniden boyutlandırma başlangıç kontrolü",taskResizeEndHandle:"Görev yeniden boyutlandırma sonu kontrolü"},"oj-ojLegend":{componentName:"Açıklama",tooltipExpand:"Genişlet",tooltipCollapse:"Daralt"},"oj-ojNBox":{highlightedCount:"{0}/{1}",labelOther:"Diğer",labelGroup:"Grup",labelSize:"Boyut",labelAdditionalData:"Ek Veriler",componentName:"{0} Kutusu"},"oj-ojPictoChart":{componentName:"Resim Grafik"},"oj-ojSparkChart":{componentName:"Grafik"},"oj-ojSunburst":{labelColor:"Renk",labelSize:"Boyut",tooltipExpand:"Genişlet",tooltipCollapse:"Daralt",componentName:"Güneş Işığı"},"oj-ojTagCloud":{componentName:"Etiket Kümesi"},"oj-ojThematicMap":{componentName:"Temalı Harita",areasRegion:"Bölgeler",linksRegion:"Bağlantılar",markersRegion:"İşaretleyiciler"},"oj-ojTimeAxis":{componentName:"Zaman Ekseni"},"oj-ojTimeline":{componentName:"Zaman Çizelgesi",accessibleItemDesc:"Açıklama {0}.",accessibleItemEnd:"Bitiş saati {0}.",accessibleItemStart:"Başlangıç saati {0}.",accessibleItemTitle:"Başlık {0}.",labelSeries:"Seri",tooltipZoomIn:"Yakınlaştır",tooltipZoomOut:"Uzaklaştır",labelStart:"Başlangıç",labelEnd:"Bitiş",labelDate:"Tarih",labelTitle:"Başlık",labelDescription:"Tanımlama"},"oj-ojTreemap":{labelColor:"Renk",labelSize:"Boyut",tooltipIsolate:"Yalıt",tooltipRestore:"Geri Yükle",componentName:"Ağaç Haritası"},"oj-dvtBaseComponent":{labelScalingSuffixThousand:"Bin",labelScalingSuffixMillion:"Mlyn",labelScalingSuffixBillion:"Mlyr",labelScalingSuffixTrillion:"Trlyn",labelScalingSuffixQuadrillion:"Ktrlyn",labelInvalidData:"Geçersiz veri",labelNoData:"Görüntülenecek veri yok",labelClearSelection:"Seçimi Temizle",labelDataVisualization:"Veri Görselleştirmesi",stateSelected:"Seçildi",stateUnselected:"Seçim Kaldırıldı",stateMaximized:"Büyütüldü",stateMinimized:"Küçültüldü",stateExpanded:"Genişletildi",stateCollapsed:"Daraltıldı",stateIsolated:"Ayrıldı",stateHidden:"Gizlendi",stateVisible:"Görünür",stateDrillable:"Detaylandırılabilir",labelAndValue:"{0}: {1}",labelCountWithTotal:"{0} /{1}"},"oj-ojNavigationList":{defaultRootLabel:"Gezinme Listesi",hierMenuBtnLabel:"Hiyerarşik Menü düğmesi",selectedLabel:"seçildi",previousIcon:"Geri",msgFetchingData:"Veriler Alınıyor...",msgNoData:"Görüntülenecek öğe yok.",overflowItemLabel:"Daha Fazla",accessibleReorderTouchInstructionText:"Çift dokunup basılı tutun. Sesi duyduğunuzda yeniden düzenlemek için sürükleyin.",accessibleReorderBeforeItem:"{item} öncesinde",accessibleReorderAfterItem:"{item} sonrasında",labelCut:"Kes",labelPasteBefore:"Öncesine Yapıştır",labelPasteAfter:"Sonrasına Yapıştır",labelRemove:"Kaldır",removeCueText:"Kaldırılabilir"},"oj-ojSlider":{noValue:"ojSlider değere sahip değil",maxMin:"Maksimum değer minimum değerden küçük veya minumum değere eşit olmamalıdır",startEnd:"value.start değeri, value.end değerinden büyük olmamalıdır",valueRange:"Değer minimum ile maksimum aralığında olmalıdır",optionNum:"{option} seçeneği sayı değildir",invalidStep:"Geçersiz adım; adım > 0 olmalıdır",lowerValueThumb:"daha düşük değer küçük resmi",higherValueThumb:"daha yüksek değer küçük resmi"},"oj-ojDialog":{labelCloseIcon:"Kapat"},"oj-ojPopup":{ariaLiveRegionInitialFocusFirstFocusable:"Açılır pencereye giriliyor. Açılır pencere ve ilişkili kontrol arasında gezinmek için F6 tuşuna basın.",ariaLiveRegionInitialFocusNone:"Açılır pencere açıldı. Açılır pencere ve ilişkili kontrol arasında gezinmek için F6 tuşuna basın.",ariaLiveRegionInitialFocusFirstFocusableTouch:"Açılır pencereye giriliyor. Açılır pencere, içindeki son bağlantıya gidilerek kapatılabilir.",ariaLiveRegionInitialFocusNoneTouch:"Açılır pencere açıldı. Açılır pencere içinde odak kurmak için sonraki bağlantıya gidin.",ariaFocusSkipLink:"Açılan pencereye gitmek için çift tıklayın.",ariaCloseSkipLink:"Açılan pencereyi kapatmak için çift tıklayın."},"oj-ojRefresher":{ariaRefreshLink:"İçeriği yenilemek için bağlantıyı etkinleştir",ariaRefreshingLink:"İçerik yenileniyor",ariaRefreshCompleteLink:"Yenileme tamamlandı"},"oj-ojSwipeActions":{ariaShowStartActionsDescription:"Başlangıç eylemlerini göster",ariaShowEndActionsDescription:"Bitiş eylemlerini göster",ariaHideActionsDescription:"Eylemleri gizle"},"oj-ojIndexer":{indexerCharacters:"A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z",indexerOthers:"#",ariaDisabledLabel:"Eşleşen grup başlığı yok",ariaOthersLabel:"sayı",ariaInBetweenText:"{first} ile {second} arasında",ariaKeyboardInstructionText:"Değer seçmek için Enter tuşuna basın.",ariaTouchInstructionText:"İşaret moduna girmek için çıft tıklayıp basılı tutun, ardından aşağı veya yukarı sürükleyerek değeri ayarlayın."},"oj-ojMenu":{labelCancel:"İptal",ariaFocusSkipLink:"Odak menü içinde. Çift tıklayarak veya kaydırarak odağı ilk menü öğesine taşıyın."},"oj-ojColorSpectrum":{labelHue:"Ton",labelOpacity:"Opaklık",labelSatLum:"Doygunluk/Parlaklık",labelThumbDesc:"Renk yelpazesi dört yönlü kaydırıcı."},"oj-ojColorPalette":{labelNone:"Yok"},"oj-ojColorPicker":{labelSwatches:"Örnekler",labelCustomColors:"Özel Renkler",labelPrevColor:"Önceki Renk",labelDefColor:"Renk Öndeğeri",labelDelete:"Sil",labelDeleteQ:"Silinsin mi?",labelAdd:"Ekle",labelAddColor:"Renk ekle",labelMenuHex:"Onaltılık",labelMenuRgba:"RGBa",labelMenuHsla:"HSLa",labelSliderHue:"Ton",labelSliderSaturation:"Doygunluk",labelSliderSat:"Doy",labelSliderLightness:"Işık",labelSliderLum:"Parlaklık",labelSliderAlpha:"Alfa",labelOpacity:"Opaklık",labelSliderRed:"Kırmızı",labelSliderGreen:"Yeşil",labelSliderBlue:"Mavi"},"oj-ojFilePicker":{dropzoneText:"Dosyaları buraya bırakın veya tıklayarak karşıya yükleyin",singleFileUploadError:"Bir seferde karşıya bir tek dosya yükleyin.",singleFileTypeUploadError:"Karşıya yükleyemeyeceğiniz dosya tipi: {fileType}.",multipleFileTypeUploadError:"Karşıya yükleyemeyeceğiniz dosya tipleri: {fileTypes}.",dropzonePrimaryText:"Sürükle ve Bırak",secondaryDropzoneText:"Bir dosya seçin veya buraya bir dosya bırakın.",secondaryDropzoneTextMultiple:"Dosya seçin veya buraya bırakın.",unknownFileType:"bilinmeyen"},"oj-ojProgressbar":{ariaIndeterminateProgressText:"Devam Ediyor"},"oj-ojMessage":{labelCloseIcon:"Kapat",categories:{error:"Hata",warning:"Uyarı",info:"Bilgi",confirmation:"Teyit"}},"oj-ojSelector":{checkboxAriaLabel:"Onay Kutusu seçimi {rowKey}"},"oj-ojMessages":{labelLandmark:"Mesajlar",ariaLiveRegion:{navigationFromKeyboard:"Mesajlar bölgesine giriliyor. Önceki odaklanılan öğeye gitmek için F6 tuşuna basın.",navigationToTouch:"Mesajlar bölgesinde yeni mesajlar var. Mesajlara gitmek için rotor üzerinden sesi kullanın.",navigationToKeyboard:"Mesajlar bölgesinde yeni mesajlar var. En yeni mesaj bölgesine F6 tuşuna basın.",newMessage:"Mesaj kategorisi {category}. {summary}. {detail}."}},"oj-ojConveyorBelt":{tipArrowNext:"İleri",tipArrowPrevious:"Geri"}});