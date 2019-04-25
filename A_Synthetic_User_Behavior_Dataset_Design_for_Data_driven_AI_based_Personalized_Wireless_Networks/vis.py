#!/usr/bin/env python
# coding: utf-8


import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import matplotlib

def heatmap_plot(df,x,path):
    #!pip install biokit
    # Drop unrelevant columns 
    """
    Inputs= df,x, path
    df---> the dataframe 
    x--> list of coolums to be dropped  
    Path---> the path to store the heatmap plot 
    
    """
    
    for i in range(len(x)):
         del  df[x[i]]
    
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    for x in df.columns:
        if df[x].dtypes=='object':
           df[x]=le.fit_transform(df[x])

    
    from biokit.viz import corrplot
    cor=df.corr(method='kendall')
    # {‘pearson’, ‘kendall’, ‘spearman’}
    c = corrplot.Corrplot(cor)
    

    c.plot(colorbar=True, method='square', shrink=.99 ,rotation=90)
   




def loc_act_plot(df,loc,path):
    

        sns.set_style("whitegrid")

        data=df[np.logical_or(np.array(df['Location name']==loc[0]),np.array(df['Location name']==loc[1] ))]
        ax = sns.countplot(x="Location name", hue="Activity", data=data,palette="Set3",saturation=0.75)
        fig = ax.get_figure()
        fig.savefig(path+'_act_plot.jpg',bbox_inches='tight')





def loc_time_per(df,path):

    sns.set_style("white")

    TLD=pd.DataFrame({'time':df['Time period'],'location':df['Location name'],'day':df['Day'],'date':df['Date']},columns=['time','location','day','date'])
    from collections import Counter
    labels_t, values_t = zip(*Counter(TLD['time']).items())
    labels_l, values_l = zip(*Counter(TLD['location']).items())
    labels_d, values_d = zip(*Counter(TLD['date']).items())


    tnum=len(labels_t)
    lnum=len(labels_l)

    Stacked_hist_df=pd.DataFrame({'Time':[""]*tnum*lnum,'Location':[""]*tnum*lnum,'Count':np.zeros(tnum*lnum)},columns=['Time','Location','Count'])
    x=0
    for i in range(tnum):
        for j in range(lnum):
            Stacked_hist_df.at[x,'Time']=labels_t[i]
            Stacked_hist_df.at[x,'Location']=labels_l[j]
            TLPF=TLD.loc[(TLD['time']==labels_t[i] )]
            TLPF=TLPF.loc[(TLPF['location']==labels_l[j] )]
            TLPF=TLPF.loc[(TLPF['date']==labels_d[0])] 

            Stacked_hist_df.at[x,'Count']=len(TLPF)

            x=x+1

    #---------------------------------------------------------------------------------------------- HERE       



    L=['Time']
    #L=L.append([""]*lnum)

    Stacked_hist_df_total_time=pd.DataFrame({'Time':[""]*tnum,'Group':np.arange(1,tnum+1), 'Count_total':np.zeros(tnum)})
    for i in range (1,lnum+1) : 
             e=pd.Series(np.zeros(tnum))                                
             Stacked_hist_df_total_time['L'+str(i)] = e                                 
             L.append('L'+str(i)  )                           
    L.append('Count_total')
    L.append('Group')


    Stacked_hist_df_total_time = Stacked_hist_df_total_time[L]

    x=0
    for i in range(tnum):
            Stacked_hist_df_total_time.at[i,'Time']=labels_t[i]        
            TLPF=TLD.loc[(TLD['time']==labels_t[i] )]
            Stacked_hist_df_total_time.at[i,'Count_total']=len(TLPF)

            for j in range(lnum):
                 Stacked_hist_df_total_time.iat[i,j+1]=Stacked_hist_df.iat[x,2]
                 x=x+1
                 j

    col=['#8dd3c7',
    '#ffffb3',
    '#bebada',
    '#fb8072',
    '#80b1d3',
    '#fdb462',
    '#fb9a99',
    '#b3de69',
    '#fccde5',
    '#d9d9d9']        

    plt.figure(figsize=(16,8))   
    # Data
    r = [0,1,2,3,4,5] 


    # From raw value to percentage
    totals=Stacked_hist_df_total_time['Count_total']


    LV={}                                     
    for num in range (lnum):
       LV[num+1]= [i / j *100 for i,j in zip(Stacked_hist_df_total_time[L[num+1]], totals)]



    # plot
    barWidth = 0.9
    names = (labels_t[0],labels_t[1],labels_t[2],labels_t[3],labels_t[4],labels_t[5])

    # Create green Bars

    plt.bar(r, LV[1], color=col[0], edgecolor='white', width=barWidth)
    plt.bar(r,LV[2], bottom=  LV[1], color=col[1], edgecolor='white', width=barWidth)



    pltvar={}
    pltvar[3]='plt.bar(r, LV[3], bottom=[i+j for i,j in zip(LV[1], LV[2])], color=col[2], edgecolor="white", width=barWidth)'
    pltvar[4]='plt.bar(r, LV[4], bottom=[i+j+k for i,j,k in zip(LV[1], LV[2],LV[3])], color=col[3], edgecolor="white", width=barWidth)'
    pltvar[5]='plt.bar(r, LV[5], bottom=[i+j+k+f for i,j,k,f in zip(LV[1], LV[2],LV[3],LV[4])], color=col[4], edgecolor="white", width=barWidth)'
    pltvar[6]='plt.bar(r, LV[6], bottom=[i+j+k+f+g for i,j,k,f,g in zip(LV[1], LV[2],LV[3],LV[4],LV[5])], color=col[5], edgecolor="white", width=barWidth)'
    pltvar[7]='plt.bar(r, LV[7], bottom=[i+j+k+f+g+p for i,j,k,f,g,p in zip(LV[1], LV[2],LV[3],LV[4],LV[5],LV[6])], color=col[6], edgecolor="white", width=barWidth)'
    pltvar[8]='plt.bar(r, LV[8], bottom=[i+j+k+f+g+p+o for i,j,k,f,g,p,o in zip(LV[1], LV[2],LV[3],LV[4],LV[5],LV[6],LV[7])], color=col[7], edgecolor="white", width=barWidth)'
    pltvar[9]='plt.bar(r, LV[9], bottom=[i+j+k+f+g+p+o+t for i,j,k,f,g,p,o,t in zip(LV[1], LV[2],LV[3],LV[4],LV[5],LV[6],LV[7],LV[8])], color=col[8], edgecolor="white", width=barWidth)'
    pltvar[10]='plt.bar(r,LV[10], bottom=[i+j+k+f+g+p+o+t+y for i,j,k,f,g,p,o,t,y in zip(LV[1], LV[2],LV[3],LV[4],LV[5],LV[6],LV[7],LV[8],LV[9])], color=col[9], edgecolor="white", width=barWidth)'

    for i in range (3,lnum+1):    
         eval(pltvar[i])


    # Custom x axis
    plt.xticks(r, names, fontsize=18)
    plt.xlabel("Time period", fontsize=18)
    plt.ylabel("Percentage", fontsize=18)

    choice=sns.color_palette(col, len(labels_l))
        # Create the legend patches
    legend_patches = [matplotlib.patches.Patch(color=C, label=L) for
                          C, L in zip(choice,
                                      labels_l)]
        # Plot the legend
    legend=plt.legend(handles=legend_patches,loc='center left', bbox_to_anchor=(1, 0.5),title='Location', prop={'size': 14})
    plt.setp(legend.get_title(),fontsize=18)
    plt.savefig(path,bbox_inches='tight')
    #plt.show()




def count_plot_per(dfsat): 
    count=dfsat.value_counts(False)
    count=count.sort_index(axis=0, level=None, ascending=True, inplace=False, sort_remaining=True)
    print(count)
    count=np.array(count )
    data=[0,0,0,0,0,0]
    #compute percentages 
    for i in range(len(count)):
         data[i]=(count[i]/np.sum(count))*100
    
    people = 'A'
    segments = 7

    # generate some multi-dimensional data & arbitrary labels
    #data = [30, 30 ,30,5,5]
    #percentages = [30, 30 ,30,10]
    y_pos = np.arange(len(people))

    fig = plt.figure(figsize=(10,1))
    ax = fig.add_subplot(111)

    colors =  col=['#8dd3c7',
        '#ffffb3',
        '#bebada',
        '#fb8072',
        '#80b1d3',
        '#fdb462',
       # '#fb9a99',
        #'#b3de69',
        #'#fccde5',
        #'#d9d9d9'
                  ]
    patch_handles = []
    left = np.zeros(len(people)) # left alignment of data starts at zero
    for i, d in enumerate(data):
        patch_handles.append(ax.barh(y_pos, d, 
          color=colors[i%len(colors)], align='center', 
          left=left))
        # accumulate the left-hand offsets
        left += d

    # go through all of the bar segments and annotate
    for j in range(len(patch_handles)):
        for i, patch in enumerate(patch_handles[j].get_children()):
            bl = patch.get_xy()
            x = 0.5*patch.get_width() + bl[0]
            y = 0.5*patch.get_height() + bl[1]
            #ax.text(x,y, "%d%%" % (percentages[i,j]), ha='center')

    ax.set_yticks(y_pos)
    ax.set_yticklabels("Satisfaction Values percentage",'')
    ax.set_xlabel('Percentage')

    plt.show()



